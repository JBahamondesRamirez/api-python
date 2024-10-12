from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEmbeddings
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from db.models.chatbot import Message
import os


model = HuggingFaceEmbeddings(model_name="hiiamsid/sentence_similarity_spanish_es", model_kwargs={ "trust_remote_code": True })
client = MongoClient("mongodb+srv://dbuser:ñandu@cluster0.eo1th.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
collection = client["rag_db"]["test"]
os.environ["HF_TOKEN"] = "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"
vector_store = MongoDBAtlasVectorSearch(
    embedding = model,
    collection = collection,
    index_name = "vector_index"
)
retriever = vector_store.as_retriever(search_type = "similarity")
llm = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.2")


async def generate_response(message:Message):
        question_text = message.text 
        prompt = PromptTemplate.from_template("""
        Responda la siguiente pregunta según el contexto dado.
        Pregunta: {question}
        Contexto: {context}
        """)
        context_docs = retriever.get_relevant_documents(question_text)
        context_text = "\n".join([doc.page_content for doc in context_docs])
        rag_chain = ({ "context": RunnablePassthrough(),"question": RunnablePassthrough() }| prompt | llm | StrOutputParser() )
        response = rag_chain.invoke({"context": context_text, "question": question_text})

        return response
