import os
import sys
import constants

from langchain_community.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import ChatOpenAI
# from langchain_community.chat_models import ChatOpenAI
# from langchain_community.llms import openai
# from langchain_community.chat_models import AzureChatOpenAI

os.environ["OPENAI_API_KEY"] = constants.APIKEY
# os.environ["OPENAI_API_TYPE"] = "azure"

# Must change
query = sys.argv[1]

loader = DirectoryLoader("data", glob="*.*")
index = VectorstoreIndexCreator().from_loaders([loader])

print(index.query(query, llm=ChatOpenAI))
