import pytesseract
from PIL import Image
from PyPDF2 import PdfReader
import docx
import pandas as pd
import sqlite3
import whisper
import os
import chromadb
from sentence_transformers import SentenceTransformer

# Initialize once
chroma_client = chromadb.PersistentClient(path="../vector_store")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  # lightweight + fast

def extract_text_from_file(path):
    ext = path.split('.')[-1].lower()
    try:
        if ext == "pdf":
            return " ".join([page.extract_text() for page in PdfReader(path).pages])
        elif ext == "txt":
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        elif ext == "docx":
            return "\n".join([p.text for p in docx.Document(path).paragraphs])
        elif ext == "xlsx":
            df = pd.read_excel(path)
            return df.to_csv(index=False)
        elif ext == "db":
            return extract_sqlite(path)
        elif ext in ["jpg", "jpeg", "png"]:
            return pytesseract.image_to_string(Image.open(path))
        elif ext in ["mp4", "mp3", "wav"]:
            return transcribe_media(path)
    except Exception as e:
        print(f"⚠️ Error extracting {ext} file: {e}")
    return ""

def extract_sqlite(path):
    conn = sqlite3.connect(path)
    text = ""
    for table in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
        df = pd.read_sql_query(f"SELECT * FROM {table[0]}", conn)
        text += df.to_csv(index=False)
    return text

def transcribe_media(path):
    model = whisper.load_model("base")
    result = model.transcribe(path)
    return result["text"]

def embed_and_store(text, user_id):
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    embeddings = embedding_model.encode(chunks).tolist()

    collection_name = f"user_{user_id}_docs"
    try:
        chroma_client.delete_collection(name=collection_name)
    except:
        pass

    collection = chroma_client.get_or_create_collection(name=collection_name)
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"{user_id}_{i}" for i in range(len(chunks))]
    )
    print(f"[Chroma] Stored {len(chunks)} chunks for user {user_id}")

def retrieve_relevant_chunks(user_id, query):
    collection_name = f"user_{user_id}_docs"
    try:
        collection = chroma_client.get_collection(name=collection_name)
        query_embedding = embedding_model.encode([query])[0].tolist()
        results = collection.query(query_embeddings=[query_embedding], n_results=3)
        return "\n".join(results["documents"][0])
    except Exception as e:
        print(f"[Chroma] Retrieval failed: {e}")
        return ""
