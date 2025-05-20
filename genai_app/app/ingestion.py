import os
import tempfile
import shutil
import pandas as pd
from flask import current_app
from utils import extract_text_from_file, embed_and_store
from memory_store import store_user_data

def process_file(file_storage, user_id: str) -> dict:
    """
    Save uploaded file to temp, extract text or table, store in memory,
    embed/store via utils, and return status + excerpt or error.
    """
    temp_dir = tempfile.mkdtemp()
    filename = file_storage.filename
    path = os.path.join(temp_dir, filename)
    file_storage.save(path)

    ext = os.path.splitext(filename)[1][1:].lower()
    try:
        if ext in {"xlsx", "xls"}:
            # Read Excel with appropriate engine
            engine = "openpyxl" if ext == "xlsx" else "xlrd"
            df = pd.read_excel(path, engine=engine)
            store_user_data(user_id, df)
            text = df.to_csv(index=False)
        else:
            # All other types via unified extractor
            text = extract_text_from_file(path)
            if not text:
                raise ValueError("Empty text extraction")
            store_user_data(user_id, text)

        # Embed and persist vectors
        embed_and_store(text, user_id)
        return {"status": "success", "text_excerpt": text[:300]}

    except Exception as e:
        current_app.logger.warning(f"⚠️ Error extracting {ext} file: {e}")
        return {"status": "error", "message": f"Error extracting {ext}: {e}"}

    finally:
        # Clean up temp files
        shutil.rmtree(temp_dir, ignore_errors=True)
