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
from langchain_openai import OpenAIEmbeddings
from pymongo import MongoClient


@api_view(['POST'])
@csrf_exempt
def loadContext(request):
    print('loading Context...')
    user_id = request.data.get('user_id')
    context_name = request.data.get('context_name')
    context = request.data.get('context')

    to_file(context)

    os.environ["OPENAI_API_KEY"] = constants.APIKEY # TODO - encrypt
    ATLAS_CONNECTION_STRING = constants.ATLASSRV
    client = MongoClient(ATLAS_CONNECTION_STRING)
    db_name = "langchain_db"
    collection_name = user_id+"_"+context_name
    atlas_collection = client[db_name][collection_name]
    vector_search_index = "vector_index"

    loader = DirectoryLoader("data", glob="*.*", show_progress=True)
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
    
    delete_file()
      
    return HttpResponse("OK")

def to_file(content):
    output_file = Path("data/context.txt")
    output_file.parent.mkdir(exist_ok=True, parents=True)
    output_file.write_text(content)
    return 

def delete_file():
    os.remove("data/context.txt")

@api_view(['POST'])
@csrf_exempt
def getContexts(request):
    print('getting Contexts...')
    user_id = request.data.get('user_id')

    ATLAS_CONNECTION_STRING = constants.ATLASSRV
    client = MongoClient(ATLAS_CONNECTION_STRING)
    db_name = "langchain_db"
    db = client.get_database(db_name)
    user_filter = {"name": {"$regex": user_id+"_."}}
    collection = db.list_collection_names(filter=user_filter)
    collection.sort()
    return Response(collection, status=status.HTTP_200_OK)
