from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain_google_vertexai import VertexAI

import os
from dotenv import load_dotenv

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


        #-----Konwersacja z pamięcią
        self.converastion_template = '''
                Jesteś pomocnym asystentem w sklepie internetowym, którego zadaniem jest porównywanie produktów, o które jesteś pytany. Twoje odpowiedzi muszą zawsze bezpośrednio odpowiadać na pytanie i zapewniać najlepsze możliwe rozwiązanie, oparte na danym kontekście, historii konwersacji i pytaniu. Pisz ciągłym tekstem, bez zbędnych znaków i nowych linii.
                
                W kontekście znajduje się url produktu pod nazwą "url", wyciągnij wszystkie url'e z kontekstu i zwróć je na końcu odpowiedzi.
                Zwróć odpowiedź na pytanie i na koniec odpowiedzi podaj wszystkie url'e z kontekstu. Odpowiedz NIE moze byc w markdownie.
                Historia konwersacji:
                {history}
                '''
        self.system_message_prompt = SystemMessagePromptTemplate.from_template(self.converastion_template)
        self.human_message_prompt = HumanMessagePromptTemplate.from_template(self.human_template)
        self.conversation_chain =  ConversationChain(
            llm = self.gemini,#self.conversation_chat,
            memory=ConversationSummaryBufferMemory(llm=self.gemini, max_token_limit=60, human_prefix="Customer"),#k=2, return_messages=True,
            verbose=True,
            prompt=ChatPromptTemplate.from_messages([self.system_message_prompt, self.human_message_prompt]),
        )
        
    def conversation(self, message: str,  searched_data: dict):
        print("wyszukane dane: ",searched_data)
        input = f'''
          Pytanie: {message}
          Kontekst: {searched_data}
        '''
        output = self.conversation_chain.predict(input = input)
        print("output: ", output)
        return output


    def ask_chat(self, message: str, searched_data: dict):
        system_message_prompt = SystemMessagePromptTemplate.from_template(self.template)
        human_message_prompt = HumanMessagePromptTemplate.from_template(self.human_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )
        answer = self.chat.invoke(
            chat_prompt.format_prompt(
                context=searched_data, question=message
            ).to_messages())
        return answer.content

