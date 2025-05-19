import os
import sqlite3
import pandas as pd
from PIL import Image

# Base directory for all FAISS stores
EMBED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "vector_store"))
os.makedirs(EMBED_DIR, exist_ok=True)

def extract_text_from_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    if ext == "pdf":
        from PyPDF2 import PdfReader
        reader = PdfReader(path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if ext == "txt":
        return open(path, "r", encoding="utf-8").read()

    if ext == "docx":
        import docx
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs)

    if ext in ("xlsx", "xls"):
        df = pd.read_excel(path)
        return df.to_csv(index=False)

    if ext == "db":
        return _extract_sqlite(path)

    if ext in ("jpg", "jpeg", "png"):
        try:
            import pytesseract
        except ImportError:
            raise RuntimeError("Please install pytesseract to extract text from images.")
        return pytesseract.image_to_string(Image.open(path))

    if ext in ("mp4", "mp3", "wav", "m4a"):
        return _transcribe_media(path)

    return ""

def _extract_sqlite(path: str) -> str:
    conn = sqlite3.connect(path)
    chunks = []
    for (table_name,) in conn.execute("SELECT name FROM sqlite_master WHERE type='table'"):
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        chunks.append(df.to_csv(index=False))
    conn.close()
    return "\n".join(chunks)

def _transcribe_media(path: str) -> str:
    try:
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(path)
        return result.get("text", "")
    except Exception as e:
        raise RuntimeError(f"Media transcription failed: {e}")

def embed_and_store(text: str, user_id: str):
    """
    Splits text into 1,000‐char chunks, embeds with OpenAIEmbeddings,
    and saves a local FAISS index under vector_store/{user_id}_store
    """
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import FAISS

    embeddings = OpenAIEmbeddings()
    chunks = [text[i : i + 1000] for i in range(0, len(text), 1000)]

    index = FAISS.from_texts(chunks, embeddings)
    user_dir = os.path.join(EMBED_DIR, f"{user_id}_store")
    os.makedirs(user_dir, exist_ok=True)
    index.save_local(user_dir)
