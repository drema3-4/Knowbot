from langchain_google_genai import ChatGoogleGenerativeAI
from ..core.config import settings
from langchain_core.prompts import PromptTemplate
from ..core.prompts import PROMPT_TEMPLATE, PROMPT_TEMPLATE_INPUT_VARIABLES
from langchain_classic.chains.retrieval_qa.base import RetrievalQA


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
        llm = ChatGoogleGenerativeAI(**self.llm_settings.to_langchain_params())
        self.chain = RetrievalQA.from_llm(
            llm=llm,
            retriever=self.retriever,
            prompt=self.prompt
        )

    def query(self, question):
        return self.chain.run(question)