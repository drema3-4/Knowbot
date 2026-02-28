# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_openai import ChatOpenAI

from core.config import settings
from core.prompts import PROMPT_TEMPLATE, PROMPT_TEMPLATE_INPUT_VARIABLES


class RAGEngine:
    def __init__(self,
        retriever
    ):
        self.retriever = retriever
        self.llm_settings = settings.llm
        self.prompt = PromptTemplate(
            template=PROMPT_TEMPLATE,
            input_variables=PROMPT_TEMPLATE_INPUT_VARIABLES
        )
        self.__init_chain__()    

    def __init_chain__(self):
        # self.llm = ChatGoogleGenerativeAI(**self.llm_settings.get_llm_settings())
        self.llm = ChatOpenAI(**self.llm_settings.get_llm_settings())
        self.chain = RetrievalQA.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            prompt=self.prompt
        )

    def query(self, question):
        return self.chain.run(question)