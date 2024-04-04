from typing import List
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain_google_vertexai import VertexAI

import os
from dotenv import load_dotenv

class Categories(BaseModel):
    categories: List[str] = Field(description="Kategorie")

class EcommerceAssistant:
    def __init__(self, temperature=0.5):
        load_dotenv()
        self.chat = ChatOpenAI(temperature=temperature, openai_api_key=os.environ["OPENAI_API_KEY"])
        self.conversation_chat = OpenAI(temperature=temperature, 
                                        openai_api_key=os.environ["OPENAI_API_KEY"],
                                        )
        self.gemini = VertexAI(model_name="gemini-pro")
        self.template = '''
        You are a helpful assistant in an ecommerce shop, tasked with addressing customer inquiries based on the context provided. Your responses must always directly answer the question and provide the best possible solution based on the given context and query.
        Context: {context}
        '''
        self.human_template = "{input}"

        self.parser = JsonOutputParser(pydantic_object=Categories)

        #-----Konwersacja z pamięcią
        self.converastion_template_start = '''
                Jesteś pomocnym asystentem w sklepie internetowym. Twoim zadaniem jest zwrócenie tylko i wyłącznie tych kategorii produktu lub produktów o które dotyczyło zapytanie uzytkownika. Musisz wybrać z ponizej podanych kategorii.

                Kategorie: [Komputery, Laptopy, Podzespoły komputerowy, Gaming, Smartfony i Smartwatche, Telewizory i audio, Foto i kamery, ADG duze, ADG małe, Dom i ogród, Biuro i firma, Sport i turystyka, Zabawki i dziecko, Uroda i zdrowie, Kultura i rozrywka, Supermarket]

                {format_intructions}

                Zapytanie: {query}
                '''
        self.converastion_template = '''
                Jesteś pomocnym asystentem w sklepie internetowym, którego zadaniem jest odpowiadanie i udzielanie informacji na tematy, o które jesteś pytany. Twoje odpowiedzi muszą zawsze bezpośrednio odpowiadać na pytanie i zapewniać najlepsze możliwe rozwiązanie, oparte na danym kontekście, historii konwersacji i pytaniu. Pisz ciągłym tekstem, bez zbędnych znaków i nowych linii.
                
                Zwróć odpowiedź na pytanie tłumacząc swój wybór na podstawie uzyskanego kontekstu, uzytkownik ma się dowiedzieć jak najwięcej potrzebnych informacji. Na koniec odpowiedzi podaj wszystkie url'e z kontekstu. Odpowiedz NIE moze byc w markdownie. Odpowiedź musi zawierać jedynie tekst i kropki.

                Historia konwersacji:
                {history}
                '''
        self.system_message_prompt = SystemMessagePromptTemplate.from_template(self.converastion_template)
        self.human_message_prompt = HumanMessagePromptTemplate.from_template(self.human_template)
        self.conversation_chain =  ConversationChain(
            llm = self.gemini,#self.conversation_chat,
            memory=ConversationSummaryBufferMemory(llm=self.gemini, max_token_limit=60, human_prefix="Customer"),#k=2, 
            verbose=True,
            # output_parser=self.parser,
            prompt=ChatPromptTemplate.from_messages([self.system_message_prompt, self.human_message_prompt]),
        )
    
    def ask_chat_categories(self, message: str):
        chat_prompt = PromptTemplate(
            template= self.converastion_template_start,
            input_variables= ["query"],
            partial_variables= {"format_intructions": self.parser.get_format_instructions()}
        )
        chain = LLMChain(
            llm=self.chat,
            verbose=True,
            prompt = chat_prompt, 
            output_parser= self.parser  
        )
        response = chain.predict(query=message)
        print("ODPOWIEDZ KATEGORII", response)

        # FILTERS
        len_filters = len(response["categories"])
        if len_filters == 0:
            return None
        filters = ""
        for (idx, filter) in enumerate(response["categories"]):
            if idx == len_filters - 1:
                filters += f"cat_level_2 == '{filter}'"
            else:
                filters += f"cat_level_2 == '{filter}' or "

        return filters
        

    def conversation(self, message: str,  searched_data: dict):
        print("wyszukane dane: ",searched_data)
        input = f'''
          Pytanie: {message}
          Kontekst: {searched_data}
        '''
        output = self.conversation_chain.predict(input = input)
        print("output: ", output)
        return output





