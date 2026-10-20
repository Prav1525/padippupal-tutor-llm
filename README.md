# PadippuPal Tutor LLM

A standalone syllabus-first teaching engine, intentionally separate from the existing PadippuPal Android app.

## Current prototype
- FastAPI tutor API with English, Tamil, and Tanglish response modes.
- Daily session memory stored in SQLite for local development.
- Optional Google Gemini API + managed Gemini File Search for semantic syllabus retrieval.
- Optional OpenAI-compatible model endpoint for later Gemma hosting or model comparisons.
- Safe fallback if a provider is not configured or fails.
- No API keys committed to source control.

> This is a prototype, not a trained foundation model. The included Grade 6 maths notes are illustrative test content, not an official textbook. Replace them with verified curriculum materials before educational release.

## Run locally
1. Use Python 3.11+.
2. Create a virtual environment and install dependencies: `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env`; add your Gemini API key locally if you want to use Google.
4. Optional: index syllabus files using `python scripts/setup_google_file_search.py`. This creates a Gemini File Search store and prints its name.
5. Set `GEMINI_FILE_SEARCH_STORE` to that store name in `.env`.
6. Start the API with `uvicorn app.main:app --reload`.
7. Open `/docs` and try `POST /v1/lesson/ask`.

The setup script indexes `.md`, `.txt`, and `.pdf` files under `SYLLABUS_DIR`. Review the rights and privacy implications of any materials before uploading them to a cloud service. Gemini File Search handles chunking, embedding, and indexing; its query-time storage/embedding work is free according to Google's current documentation, while model input/output usage and initial indexing may incur charges depending on account/tier.

## API
- `GET /health`
- `POST /v1/lesson/ask`
- `GET /v1/lesson/{session_id}/history`

Example request: `{"student_id":"demo-student","session_id":"demo-session","grade":6,"subject":"mathematics","topic":"fractions","language":"tanglish","question":"Fraction na enna?"}`

## Environment variables
- `GEMINI_API_KEY`: secret key; configure in `.env` locally or Render's environment settings, never Git.
- `GEMINI_FILE_SEARCH_STORE`: store name printed by the setup script.
- `GEMINI_MODEL`: model name (defaults to `gemini-3.8-flash` in this prototype).
- `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`: optional OpenAI-compatible alternative endpoint. This is the future integration point for hosted Gemma or another model.

## Privacy and deployment
Use synthetic learner IDs during development. Do not upload identifiable child data to model APIs. Check the current provider terms and data-use settings before sending real student conversations. The prototype uses local SQLite; production should use a separate managed database with access controls and retention/deletion policies.

## Next milestones
1. Confirm board/curriculum (e.g. Tamil Nadu State Board or CBSE) and source materials.
2. Index validated chapter content and evaluate citations/answer grounding.
3. Benchmark Gemini against one or more Gemma candidates on Tamil/Tanglish, English, math correctness, child-friendly teaching, latency, and total cost.
4. Add teacher-reviewed examples and only then evaluate LoRA/QLoRA fine-tuning.
5. Deploy as a separate service before considering Android integration.
