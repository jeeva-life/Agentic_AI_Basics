from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from model import  embed_model
from dotenv import load_dotenv
load_dotenv()

urls = [
    "https://www.google.com/search?q=langchain",
    "https://www.google.com/search?q=langgraph",
    "https://www.google.com/search?q=langchain-aws",
]

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [doc for sublist in docs for doc in sublist]

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=500, chunk_overalp=20)

doc_splits = text_splitter.split_documents(docs_list)

embed = embed_model

# create vetor store with documents
vectorestore = Chroma.from_documents(
    documents = doc_splits,
    collection_name='RAG_CHROMA',
    embedding=embed,
    persist_directory='./chroma_db',
)

#Create Retriever

retriever = vectorestore.as_retriever(k=3)
