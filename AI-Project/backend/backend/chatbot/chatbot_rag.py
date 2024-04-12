import os
import sys
import constants
import pymongo, pprint

from langchain_community.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pymongo import MongoClient
# from langchain_community.chat_models import ChatOpenAI
# from langchain_community.llms import openai
# from langchain_community.chat_models import AzureChatOpenAI

os.environ["OPENAI_API_KEY"] = constants.APIKEY
# os.environ["OPENAI_API_TYPE"] = "azure"
ATLAS_CONNECTION_STRING = constants.ATLASSRV

# Connect to your Atlas cluster
client = MongoClient(ATLAS_CONNECTION_STRING)

# Define collection and index name
db_name = "langchain_db"
collection_name = "cogitch"
atlas_collection = client[db_name][collection_name]
vector_search_index = "vector_index"

# Load the PDF
loader = PyPDFLoader("https://query.prod.cms.rt.microsoft.com/cms/api/am/binary/RE4HkJP")
# Load all files in a directory
# loader = DirectoryLoader("data", glob="*.*", show_progress=True)
data = loader.load()

# Split PDF into documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
docs = text_splitter.split_documents(data)

# Print the first document
docs[0]

# Create the vector store
vector_search = MongoDBAtlasVectorSearch.from_documents(
    documents = docs,
    embedding = OpenAIEmbeddings(disallowed_special=()),
    collection = atlas_collection,
    index_name = vector_search_index
)

# Instantiate Atlas Vector Search as a retriever
retriever = vector_search.as_retriever(
   search_type = "similarity",
   search_kwargs = {"k": 10, "score_threshold": 0.75}
)

# Define a prompt template
template = """

Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
"""
custom_rag_prompt = PromptTemplate.from_template(template)

llm = ChatOpenAI()

def format_docs(docs):
   return "\n\n".join(doc.page_content for doc in docs)

# Construct a chain to answer questions on your data
rag_chain = (
   { "context": retriever | format_docs, "question": RunnablePassthrough()}
   | custom_rag_prompt
   | llm
   | StrOutputParser()
)

# Prompt the chain
question = sys.argv[1] # whre to retrieve the input question has to change
answer = rag_chain.invoke(question)

print("Question: " + question)
print("Answer: " + answer)

# Return source documents
#documents = retriever.get_relevant_documents(question)
#print("\n\nSource documents:")
#pprint.pprint(documents)