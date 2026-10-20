# PadippuPal Tutor LLM

A standalone syllabus-first teaching engine, intentionally separate from the existing PadippuPal Android app.

## First milestone
- Grade 6 Mathematics prototype with a clearly labelled sample syllabus.
- Retrieval-first answers grounded in syllabus material.
- Session continuity stored by learner/session and calendar day.
- English, Tamil, and Tanglish response modes.
- Provider-agnostic model adapter using an OpenAI-compatible chat-completions API.
- No model keys committed to source control.

> This is a prototype, not a trained foundation model. We will benchmark model candidates and verify curriculum sources before selecting a base model or fine-tuning.

## Run locally
1. Use Python 3.11+.
2. Create a virtual environment and install dependencies from requirements.txt.
3. Copy .env.example to .env and configure an OpenAI-compatible endpoint/model if available.
4. Start with `uvicorn app.main:app --reload`.
5. Open `/docs` for the API.

Without a model endpoint, the API returns a safe syllabus-grounded fallback rather than pretending a model answered.

## API
- `GET /health`
- `POST /v1/lesson/ask`
- `GET /v1/lesson/{session_id}/history`

Example request: `{"student_id":"demo-student","session_id":"demo-session","grade":6,"subject":"mathematics","topic":"fractions","language":"tanglish","question":"Fraction na enna?"}`

## Privacy and deployment
Keep real student data and all API keys out of Git. Use synthetic learner IDs during development. The prototype stores conversation turns in a local SQLite database; production deployment should use a separately provisioned database and retention controls.

## Next milestones
1. Confirm board/curriculum and source materials.
2. Build chapter ingestion, citations, and retrieval evaluation.
3. Benchmark candidate models on Tamil/Tanglish, English, math correctness, child-safe teaching, and latency.
4. Add teacher-reviewed examples and only then evaluate LoRA/QLoRA fine-tuning.
5. Deploy as a separate service before considering any Android integration.
