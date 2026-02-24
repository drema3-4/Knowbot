from langchain_google_genai import ChatGoogleGenerativeAI
from ..core.config import settings
from langchain_classic.chains.retrieval_qa.base import RetrievalQA


class RAG_engine:
    def __init__(self, vectore_store, embeddings):
        self.vector_store = vectore_store
        self.llm_settings = settings.llm
        self.embeddings = embeddings
        self.__init_chain__()
        

    def __init_chain__(self):
        retriever = self.vector_store.as_retriever()
        llm = ChatGoogleGenerativeAI(**self.llm_settings.to_langchain_params())
        self.chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    def query(self, question):
        return self.chain.run(question)

