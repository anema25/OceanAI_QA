# backend/ingest.py
import os, json, uuid
from sentence_transformers import SentenceTransformer
from chromadb import Client
from chromadb.config import Settings
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter

MODEL_NAME = "all-MiniLM-L6-v2"  # change if you have another HF model
EMBED_MODEL = SentenceTransformer(MODEL_NAME)

CHROMA_DIR = os.path.abspath("chroma_db")

client = Client(Settings(chroma_db_impl="chromadb.db", persist_directory=CHROMA_DIR))
collection = client.get_or_create_collection("qa_kb")

def read_file(path):
    ext = path.split('.')[-1].lower()
    if ext in ['md','txt','json']:
        with open(path,'r',encoding='utf-8') as f: return f.read()
    elif ext == 'html':
        with open(path,'r',encoding='utf-8') as f:
            soup = BeautifulSoup(f, "html.parser")
            return soup.get_text(separator="\n")
    else:
        return ""

def chunk_and_index(path):
    text = read_file(path)
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_text(text)
    embeddings = EMBED_MODEL.encode(chunks).tolist()
    metadatas = [{"source_document": os.path.basename(path), "chunk_index":i} for i,_ in enumerate(chunks)]
    ids = [str(uuid.uuid4()) for _ in chunks]
    collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=chunks)
    client.persist()
    return len(chunks)
