# EduGenie: Architecture & System Workflow

## 1. Project Workflow
1. Client requests an educational task via `/templates/index.html` or direct REST API call.
2. The FastAPI application (`main.py`) validates the payload using Pydantic models.
3. The request is routed to the dedicated module (`qna.py`, `explanation_module.py`, `quiz_module.py`, `summary_module.py`, or `learning_path.py`).
4. `ai_client.py` formats the system prompt and communicates with Google Gemini API (`gemini-2.5-flash`).
5. Structured markdown/JSON responses are returned to the client interface.

## 2. Epics Coverage
- **Epic 1 (Model Selection & Architecture):** FastAPI asynchronous backend + Gemini API client with fallback support.
- **Epic 2 (Core Functionalities):** Academic Q&A, conceptual simplification, 3-question MCQ generation, passage summarization, and step-by-step learning paths.
- **Epic 3 (Frontend UI):** Jinja2 template rendering with interactive responsive cards and Swagger UI integration (`/docs`).
- **Epic 4 (Testing & Deployment):** Automated unit tests in `tests/test_app.py` using `pytest`, configured for deployment via Render (`render.yaml`, `Procfile`).
- 
