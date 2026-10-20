"""Create a Gemini File Search store and index local syllabus files.

Run locally after setting GEMINI_API_KEY. Review syllabus source rights before uploading.
"""
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY", "").strip()
if not api_key:
    raise SystemExit("Set GEMINI_API_KEY in your local .env first; do not commit the key.")

syllabus_dir = Path(os.getenv("SYLLABUS_DIR", "./syllabus"))
files = sorted(p for p in syllabus_dir.rglob("*") if p.is_file() and p.suffix.lower() in {".md", ".txt", ".pdf"})
if not files:
    raise SystemExit(f"No .md, .txt or .pdf syllabus files found in {syllabus_dir.resolve()}")

client = genai.Client(api_key=api_key)
store = client.file_search_stores.create(config={
    "display_name": "padippupal-syllabus-v1",
    "embedding_model": "models/gemini-embedding-2",
})
print(f"Created File Search store: {store.name}")
for path in files:
    print(f"Indexing {path} ...")
    operation = client.file_search_stores.upload_to_file_search_store(
        file=str(path),
        file_search_store_name=store.name,
        config={"display_name": path.name},
    )
    while not operation.done:
        time.sleep(3)
        operation = client.operations.get(operation)
    print(f"Indexed: {path.name}")

print("\nIndexing complete. Set these in Render Environment (never commit secrets):")
print("GEMINI_FILE_SEARCH_STORE=" + store.name)
print("GEMINI_MODEL=gemini-3.8-flash")
print("Keep GEMINI_API_KEY in the secret environment variable field.")
