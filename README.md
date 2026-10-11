# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a responsive learning assistant based on the supplied project documentation. It provides:
- Academic Q&A
- Beginner-friendly concept explanations
- Three-question multiple-choice quizzes with answer feedback
- Passage summaries
- Beginner-to-advanced learning paths

**Stack:** FastAPI, Python, HTML/CSS/JavaScript, Jinja2, Google Gemini API. The documentation names Gemini 1.5 Pro; this project defaults to `gemini-2.5-flash` because model availability changes over time. Set `GEMINI_MODEL` to another model enabled for your API key if necessary. Gemini access requires an internet connection and a valid API key.

## 1. Requirements
- Python 3.10 or newer
- Visual Studio Code
- Internet connection for Gemini requests
- Gemini API key from Google AI Studio

## 2. Open the project in VS Code
1. Extract the ZIP file.
2. In VS Code choose **File → Open Folder** and select the `EduGenie` folder.
3. Open **Terminal → New Terminal**.

## 3. Create a virtual environment

Windows PowerShell:
```powershell
py -m venv .venv
.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Windows Command Prompt:
```bat
py -m venv .venv
.venv\\Scripts\\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If activation is blocked on PowerShell, you can run `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`, then run Uvicorn with `.\.venv\Scripts\python.exe -m uvicorn main:app --reload`.

## 4. Configure the Gemini API key
1. Copy `.env.example` to a new file named `.env` in the project root.
2. Open `.env` and replace `put_your_api_key_here` with your real key.
3. Save the file. Do not paste your key into source code or commit `.env` to Git.

Example:
```env
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-2.5-flash
EDU_USE_LOCAL_MODEL=false
PORT=8000
```

Get the key through Google AI Studio: https://aistudio.google.com/app/apikey . Model names and API access can vary by account/region; if the default model is unavailable, use a model listed as available to your key.

## 5. Run EduGenie
With the virtual environment active:
```bash
uvicorn main:app --reload
```
Open **http://127.0.0.1:8000** in your browser. API documentation is available at **http://127.0.0.1:8000/docs**. Stop the server with Ctrl+C.

## 6. Test the app
Use each card in the browser:
1. Ask a question — `What is the difference between AI and ML?`
2. Explain a topic — `Explain photosynthesis to a beginner.`
3. Generate a quiz — paste a paragraph or enter `The Pythagorean theorem relates the sides of a right triangle.`
4. Summarize text — paste a passage of at least 20 characters.
5. Learning path — `Create a beginner learning path for SQL.`

You can also use Swagger UI at `/docs` and POST to `/api/task` with:
```json
{
  "task": "qa",
  "text": "What is machine learning?"
}
```
Allowed task values: `qa`, `explain`, `quiz`, `summarize`, `learn`.

Run automated tests (the tests mock the AI call, so they do not need an API key):
```bash
pytest -q
```

## 7. Optional local LaMini explanation model
The supplied document describes LaMini-Flan-T5-783M as a local explanation model. It is optional because it downloads a large model and needs extra disk space and RAM. The default setup uses Gemini for explanations and is easier to install.

To enable local explanations:
```bash
pip install -r requirements-local.txt
```
Then set these values in `.env`:
```env
EDU_USE_LOCAL_MODEL=true
LOCAL_MODEL_NAME=MBZUAI/LaMini-Flan-T5-783M
```
Restart the server. The first local-model run downloads model files. CPU inference can be slow. Set `EDU_USE_LOCAL_MODEL=false` to return to Gemini.

## 8. Folder structure
```text
EduGenie/
├── main.py
├── ai_client.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── requirements-local.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── tests/
    └── test_app.py
```

## Troubleshooting
- **Missing API key:** confirm `.env` is in the same folder as `main.py` and contains `GEMINI_API_KEY=...`.
- **401 / 403:** verify the key, API access, account and project settings.
- **Model not found / unavailable:** set `GEMINI_MODEL` to a model enabled for your API key.
- **429 / quota:** wait or review your API quota and billing limits.
- **Port already in use:** run `uvicorn main:app --reload --port 8001`, then visit `http://127.0.0.1:8001`.
- **Local model download/memory error:** switch `EDU_USE_LOCAL_MODEL=false` and restart.
- **Do not expose your API key:** `.env` is ignored by Git. If a key is accidentally shared, revoke it and create a replacement.

## Notes
AI responses can be inaccurate; verify important facts with trusted sources. Do not submit private or sensitive student information. This starter project does not include user accounts, database persistence, rate limiting, or production deployment hardening.

## Upload to GitHub
```bash
git init
git add .
git commit -m "EduGenie: Gemini powered learning assistant"
git branch -M main
git remote add origin https://github.com/<your-username>/EduGenie.git
git push -u origin main
```
`.env` is in `.gitignore`, so your API key is never uploaded.

## Deploy online (Render, free)
1. Push the project to GitHub (above).
2. On render.com choose **New → Blueprint** (or **Web Service**) and select the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add the environment variable `GEMINI_API_KEY` and deploy.

## API endpoints
`POST /qa`, `POST /explain`, `POST /quiz`, `POST /summarize`, `POST /learn/recommendations` and `POST /api/task`
(body: `{"task": "...", "text": "..."}`), plus `GET /health`.
