import os
import pytesseract
from PIL import Image
from PyPDF2 import PdfReader
import docx
import pandas as pd
import sqlite3
import whisper

# LangChain & Embeddings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

# Embedding setup
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
base_vectorstore_path = os.path.join("..", "vector_store")

# ----------------------------------------
# File extraction logic
# ----------------------------------------
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

# ----------------------------------------
# SQLite table text extraction
# ----------------------------------------
def extract_sqlite(path):
    conn = sqlite3.connect(path)
    text = ""
    try:
        for table in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
            df = pd.read_sql_query(f"SELECT * FROM {table[0]}", conn)
            text += df.to_csv(index=False)
    except Exception as e:
        print(f"⚠️ SQLite extract error: {e}")
    finally:
        conn.close()
    return text

# ----------------------------------------
# Transcribe media (audio/video)
# ----------------------------------------
def transcribe_media(path):
    model = whisper.load_model("base")
    result = model.transcribe(path)
    return result.get("text", "")

# ----------------------------------------
# Embed and store with LangChain + Chroma
# ----------------------------------------
def embed_and_store(text, user_id):
    chunks = split_text(text)
    documents = [Document(page_content=chunk) for chunk in chunks]

    vector_path = os.path.join(base_vectorstore_path, user_id)
    if os.path.exists(vector_path):
        # Clear previous version (optional)
        for file in os.listdir(vector_path):
            os.remove(os.path.join(vector_path, file))

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=vector_path
    )
    vectordb.persist()
    print(f"[Chroma] Stored {len(documents)} chunks for user {user_id}")

# ----------------------------------------
# Retrieve relevant chunks for query
# ----------------------------------------
def retrieve_relevant_chunks(user_id, query, k=3):
    vector_path = os.path.join(base_vectorstore_path, user_id)
    try:
        vectordb = Chroma(
            persist_directory=vector_path,
            embedding_function=embedding_model
        )
        retriever = vectordb.as_retriever(search_kwargs={"k": k})
        docs = retriever.get_relevant_documents(query)
        return "\n".join([doc.page_content for doc in docs])
    except Exception as e:
        print(f"[Chroma Retrieval Error]: {e}")
        return ""

# ----------------------------------------
# Chunking logic
# ----------------------------------------
def split_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_text(text)
