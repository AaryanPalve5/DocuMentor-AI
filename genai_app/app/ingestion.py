import os
import tempfile
import shutil
from utils import extract_text_from_file, embed_and_store
from memory_store import store_user_data

def process_file(file, user_id):
    """
    1) Save the uploaded file to a temp directory
    2) Extract text (PDF, TXT, DOCX, Excel, image OCR, media transcription)
    3) Embed and store vectors in FAISS
    4) Store raw text in memory_store for dashboards/chat
    5) Return a JSONable excerpt
    """
    temp_dir = tempfile.mkdtemp()
    try:
        path = os.path.join(temp_dir, file.filename)
        with open(path, "wb") as f:
            f.write(file.read())

        text = extract_text_from_file(path)
        if not text:
            raise ValueError("Failed to extract text from the provided file.")

        embed_and_store(text, user_id)
        store_user_data(user_id, text)

        return {
            "status": "success",
            "text_excerpt": text[:300]
        }
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
