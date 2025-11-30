# backend/retrieval.py
from sentence_transformers import SentenceTransformer
from chromadb import Client
from chromadb.config import Settings

MODEL_NAME = "all-MiniLM-L6-v2"
EMBED = SentenceTransformer(MODEL_NAME)
client = Client(Settings(chroma_db_impl="chromadb.db", persist_directory="chroma_db"))
collection = client.get_collection("qa_kb")

def retrieve(query, k=5):
    q_emb = EMBED.encode([query])[0].tolist()
    results = collection.query(query_embeddings=[q_emb], n_results=k)
    docs = []
    for docs_list, metas_list, distances in zip(results['documents'], results['metadatas'], results['distances']):
        for d,m in zip(docs_list, metas_list):
            docs.append({"text": d, "meta": m})
    return docs
