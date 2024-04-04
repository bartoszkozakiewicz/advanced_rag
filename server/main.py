import sys
sys.path.append("../vectorstore/")
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from milvus_store import MilvusStoreWithClient
from chat.ecommerce_assistant import EcommerceAssistant

import json

#Langchain
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()


#---------------INIT APP------------------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#---------------INIT DATA------------------
storeClient = MilvusStoreWithClient(csv_file_path="../vectorstore/data/products.csv")
COLLECTION_NAME="full_morele_pl"

chat = ChatOpenAI(temperature=0.5, openai_api_key=os.environ["OPENAI_API_KEY"])
EcommerceAssistant = EcommerceAssistant()
#---------------TYPES------------------
class ChatMessage(BaseModel):
    message: str


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/chat", response_model=dict)
async def getMessage(message:ChatMessage):
    print("Otrzymałem wiadomość ", message.message)
    assert message.message is not None, "Message must be provided"


    #CATEGORIES EXTRACTION - OPENAI CHAT
    filters = EcommerceAssistant.ask_chat_categories(message=message.message)

    # VECTORSTORE
    searched_data = storeClient.search(
            collection_name = COLLECTION_NAME, 
            query= message.message,
            fixed_filter = filters,
            limit = 3,
            output_fields = [ "price","cat_level_4", "cat_level_5","specification","all_variants","long_description","url"],# "url"
            search_params = None
        )
    
    #OPENAI CHAT
    answear = EcommerceAssistant.conversation(message=message.message, searched_data=searched_data)
    return {"message": answear}