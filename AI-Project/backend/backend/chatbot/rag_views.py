import os
import re
import requests
from pathlib import Path
from . import constants
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from requests.auth import HTTPDigestAuth
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import SharePointLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_cohere import ChatCohere, CohereEmbeddings
from langchain_anthropic import ChatAnthropic
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
from office365.sharepoint.client_context import AuthenticationContext

# Statefully manage chat history
store = {}
# Constant variables
AIP_DB = constants.AIPDB
ATLAS_CONNECTION_STRING = constants.ATLASSRV
ATLAS_PUB_KEY = constants.ATLAS_PK
ATLAS_K = constants.ATLAS_K
IDX_URL = constants.IDX_URL
clientAtlas = MongoClient(ATLAS_CONNECTION_STRING)
clientAipDb = MongoClient(host=AIP_DB, port=27017)

os.environ["OPENAI_API_KEY"] = constants.APIKEY
os.environ["COHERE_API_KEY"] = constants.COHERE_KEY
os.environ["ANTHROPIC_API_KEY"] = constants.ANTHROPIC_KEY

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
def loadSharepoint(request):
    print('loading Context from Sharepoint...')
    user_id = request.data.get('user_id')
    sp_link = request.data.get('sp_link')
    split = re.split("sharepoint.com", sp_link)
    embed = request.data.get('embeddings')

    client_id = request.data.get('client_id')
    client_secret = request.data.get('client_secret')
    document_library_id = request.data.get('document_library_id')
    path = request.data.get('folder_path')

    if (sp_link=='' or client_id=='' or client_secret=='' or document_library_id=='' or path==''):
       return HttpResponse(status.HTTP_400_BAD_REQUEST) 
    
    os.environ['O365_CLIENT_ID'] = client_id
    os.environ['O365_CLIENT_SECRET'] = client_secret

    context_auth = AuthenticationContext(url=sp_link)

    token = context_auth.acquire_token_for_app(client_id=client_id, client_secret=client_secret)
    print(token)
    saveAuthtoken(token)

    loader = SharePointLoader(document_library_id=document_library_id, folder_path='/'+path, auth_with_token=True)
    data = loader.load()

    os.environ['O365_CLIENT_ID'] = ''
    os.environ['O365_CLIENT_SECRET'] = ''

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    docs = text_splitter.split_documents(data)
    print(docs[0])

    db_name = "langchain_db"
    context_name = re.split("sites/", split[1])[1]
    collection_name = user_id+"_"+context_name
    atlas_collection = clientAtlas[db_name][collection_name]
    
    index_def = {
        "collectionName": collection_name,
        "database": db_name,
        "name": context_name.split('.')[0].replace(' ',''),
        "type": "vectorSearch",
        "definition": {
            "fields":[
                {
                    "type": "vector",
                    "path": "embedding",
                    "numDimensions": 1536,
                    "similarity": "cosine"
                }
            ]
        }
    }

    res = requests.post(url=IDX_URL, auth=HTTPDigestAuth(ATLAS_PUB_KEY, ATLAS_K), 
                        headers={"Content-Type": "application/json", "Accept": "application/vnd.atlas.2024-05-30+json"},
                        data=dumps(index_def))
    if (not res.ok):
       return HttpResponse(status.HTTP_405_METHOD_NOT_ALLOWED)

    if (embed=="openai"):
        embeddings = OpenAIEmbeddings(disallowed_special=())
    elif (embed=="cohere"):
        embeddings = CohereEmbeddings(model="embed-multilingual-light-v3.0")

    MongoDBAtlasVectorSearch.from_documents(
        documents = docs,
        embedding = embeddings,
        collection = atlas_collection,
        index_name = context_name.split('.')[0]
    )

    return HttpResponse(status.HTTP_200_OK)

def saveAuthtoken(token):
    output_file = Path("~/.credentials/o365_token.txt")
    output_file.parent.mkdir(exist_ok=True, parents=True)
    output_file.write_text(token)
    return 

@api_view(['POST'])
@csrf_exempt
def loadContext(request):
    print('loading Context...')
    user_id = request.data.get('user_id')
    context_name = request.data.get('context_name')
    context = request.data.get('context')
    embed = request.data.get('embeddings')

    to_file(context, user_id)

    db_name = "langchain_db"
    collection_name = user_id+"_"+context_name
    atlas_collection = clientAtlas[db_name][collection_name]

    loader = DirectoryLoader("data/"+user_id, glob="*.*", show_progress=True)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    docs = text_splitter.split_documents(data)
    print(docs[0])
    
    index_def = {
        "collectionName": collection_name,
        "database": db_name,
        "name": context_name.split('.')[0].replace(' ',''),
        "type": "vectorSearch",
        "definition": {
            "fields":[
                {
                    "type": "vector",
                    "path": "embedding",
                    "numDimensions": 1536,
                    "similarity": "cosine"
                },
                {
                    "type": "filter",
                    "path": "page"
                }
            ]
        }
    }

    res = requests.post(url=IDX_URL, auth=HTTPDigestAuth(ATLAS_PUB_KEY, ATLAS_K), 
                        headers={"Content-Type": "application/json", "Accept": "application/vnd.atlas.2024-05-30+json"},
                        data=dumps(index_def))
    if (not res.ok):
       return HttpResponse(status.HTTP_405_METHOD_NOT_ALLOWED)

    if (embed=="openai"):
        embeddings = OpenAIEmbeddings(disallowed_special=())
    elif (embed=="cohere"):
        embeddings = CohereEmbeddings(model="embed-multilingual-light-v3.0")

    MongoDBAtlasVectorSearch.from_documents(
        documents = docs,
        embedding = embeddings,
        collection = atlas_collection,
        index_name = context_name.split('.')[0]
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
    context_name = rag_conf[1].split(user_id+'_')[1]
    print(context_name)

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
            index_name = context_name
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
            output_messages_key="answer"
        )

        ans = conversational_rag_chain.invoke({'input': question}, {'configurable': {'session_id': user_id, 'llm': llm}})
        
        if (ans):
            return Response(ans["answer"], status=status.HTTP_200_OK)
        else:
            HttpResponse(status.HTTP_405_METHOD_NOT_ALLOWED)

    elif (model=="cohere"):

        llm = ChatCohere()

        db_name = "langchain_db"
        db = clientAtlas.get_database(db_name)
        filter = {"name": {"$regex": context_name}}
        coll = db.list_collection_names(filter=filter)[0]
        atlas_collection = clientAtlas[db_name][coll]

        vectorstore = MongoDBAtlasVectorSearch(
            embedding = CohereEmbeddings(model="embed-multilingual-light-v3.0"),
            collection = atlas_collection,
            index_name = context_name
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
            output_messages_key="answer"
        )

        ans = conversational_rag_chain.invoke({'input': question}, {'configurable': {'session_id': user_id, 'llm': llm}})
        
        if (ans):
            return Response(ans["answer"], status=status.HTTP_200_OK)
        else:
            HttpResponse(status.HTTP_405_METHOD_NOT_ALLOWED)

    elif (model=="anthropic"):

        llm = ChatAnthropic(model='claude-3-opus-20240229')

        db_name = "langchain_db"
        db = clientAtlas.get_database(db_name)
        filter = {"name": {"$regex": context_name}}
        coll = db.list_collection_names(filter=filter)[0]
        atlas_collection = clientAtlas[db_name][coll]

        vectorstore = MongoDBAtlasVectorSearch(
            embedding = CohereEmbeddings(model="embed-multilingual-light-v3.0"),
            collection = atlas_collection,
            index_name = context_name
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
            output_messages_key="answer"
        )

        ans = conversational_rag_chain.invoke({'input': question}, {'configurable': {'session_id': user_id, 'llm': llm}})
        
        if (ans):
            return Response(ans["answer"], status=status.HTTP_200_OK)
        else:
            HttpResponse(status.HTTP_405_METHOD_NOT_ALLOWED)