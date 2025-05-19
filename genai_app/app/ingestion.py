import os
import tempfile
import shutil
from utils import extract_text_from_file, embed_and_store
from memory_store import store_user_data

def process_file(file, user_id):
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, file.filename)
    with open(path, "wb") as f:
        f.write(file.read())

    text = extract_text_from_file(path)
    if not text:
        return {"status": "error", "message": "Text extraction failed."}

    embed_and_store(text, user_id)
    store_user_data(user_id, text)

    shutil.rmtree(temp_dir)
    return {"status": "success", "text_excerpt": text[:300]}
