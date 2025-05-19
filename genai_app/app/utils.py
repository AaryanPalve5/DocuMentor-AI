import pytesseract
from PIL import Image
from PyPDF2 import PdfReader
import docx
import pandas as pd
import sqlite3
import whisper
from moviepy.editor import VideoFileClip
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import os

embedding_model = OpenAIEmbeddings()

def extract_text_from_file(path):
    ext = path.split('.')[-1].lower()
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
    db = FAISS.from_texts(chunks, embedding_model)
    db.save_local(f"../vector_store/{user_id}_store")
