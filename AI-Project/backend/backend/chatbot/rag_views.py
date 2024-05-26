import os
from pathlib import Path
from . import constants
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pymongo import MongoClient
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from bson.json_util import dumps
from bson.json_util import loads

# Statefully manage chat history
store = {}
# Constant variables
AIP_DB = constants.AIPDB
ATLAS_CONNECTION_STRING = constants.ATLASSRV
clientAtlas = MongoClient(ATLAS_CONNECTION_STRING)
clientAipDb = MongoClient(host=AIP_DB, port=27017)

os.environ["OPENAI_API_KEY"] = constants.APIKEY # TODO - encrypt

q_prompt = ChatPromptTemplate.from_messages(
    [
            ("system", "Using your context to answer the question at the end."),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
    ]
)
qa_prompt = ChatPromptTemplate.from_messages(
    [   
        ("system", "This chatbot remebers what it previously answered to you. Here the used documents: {context}"),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

@api_view(['POST'])
@csrf_exempt
def loadContext(request):
    print('loading Context...')
    user_id = request.data.get('user_id')
    context_name = request.data.get('context_name')
    context = request.data.get('context')

    to_file(context, user_id)

    db_name = "langchain_db"
    collection_name = user_id+"_"+context_name
    atlas_collection = clientAtlas[db_name][collection_name]
    vector_search_index = "vector_index"

    loader = DirectoryLoader("data/"+user_id, glob="*.*", show_progress=True)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    docs = text_splitter.split_documents(data)

    print(docs[0])

    MongoDBAtlasVectorSearch.from_documents(
        documents = docs,
        embedding = OpenAIEmbeddings(disallowed_special=()),
        collection = atlas_collection,
        index_name = vector_search_index
    )
    
    delete_context_file(user_id)
      
    return HttpResponse(status.HTTP_200_OK)

def to_file(content, id):
    output_file = Path("data/"+id+"/context.txt")
    output_file.parent.mkdir(exist_ok=True, parents=True)
    output_file.write_text(content)
    return 

def delete_context_file(id):
    os.remove("data/"+id+"/context.txt")

@api_view(['POST'])
@csrf_exempt
def getContexts(request):
    print('getting Contexts...')
    user_id = request.data.get('user_id')

    db_name = "langchain_db"
    db = clientAtlas.get_database(db_name)
    user_filter = {"name": {"$regex": user_id+"_."}}
    collection = db.list_collection_names(filter=user_filter)
    collection.sort()
    return Response(collection, status=status.HTTP_200_OK)

@api_view(['POST'])
@csrf_exempt
def addModel(request):
    print('adding Model...')
    user_id = request.data.get('user_id')
    context_name = request.data.get('context_name')
    model = request.data.get('model')

    aip_coll_name = "ragchains"
    aip_db = clientAipDb.get_database("AIP_DB")
    aip_collection = aip_db.get_collection(aip_coll_name)
      
    result = aip_collection.insert_one({ "user" : user_id, "model_name" : model+'-'+context_name })

    if(result):
        return HttpResponse(status.HTTP_200_OK)
    else:
        return HttpResponse(status.HTTP_405_METHOD_NOT_ALLOWED)

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

@api_view(['POST'])
@csrf_exempt
def getModels(request):
    print('getting Models...')
    user_id = request.data.get('user_id')

    aip_coll_name = "ragchains"
    aip_db = clientAipDb.get_database("AIP_DB")
    aip_collection = aip_db.get_collection(aip_coll_name)
    docs = loads(dumps(aip_collection.find({ "user": user_id },{ "model_name": 1, "_id": 0 })))
    if (docs):
        return Response(str(list(docs)), status=status.HTTP_200_OK)  
    else:
        return HttpResponse(status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['POST'])
@csrf_exempt
def query(request):
    print('querying Chatbot...')
    user_id = request.data.get('user_id')
    rag_model = request.data.get('rag_model')
    question = request.data.get('query')
    rag_conf = str(rag_model).split('-')
    model = rag_conf[0]
    context_name = rag_conf[1]

    if (model=="openai"):

        llm = ChatOpenAI()

        db_name = "langchain_db"
        db = clientAtlas.get_database(db_name)
        filter = {"name": {"$regex": context_name}}
        coll = db.list_collection_names(filter=filter)[0]
        atlas_collection = clientAtlas[db_name][coll]

        vectorstore = MongoDBAtlasVectorSearch(
            embedding = OpenAIEmbeddings(disallowed_special=()),
            collection = atlas_collection,
            index_name = "vector_index"
        )   
    
        retriever = vectorstore.as_retriever(
        search_type = "similarity",
        search_kwargs = {"k": 10, "score_threshold": 0.75})

        history_aware_retriever = create_history_aware_retriever(
            llm, retriever, q_prompt
        )
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
        
        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

        ans = conversational_rag_chain.invoke({'input': question}, {'configurable': {'session_id': user_id}})
        
        if (ans):
            return Response(ans["answer"], status=status.HTTP_200_OK)
        else:
            HttpResponse(status.HTTP_405_METHOD_NOT_ALLOWED)