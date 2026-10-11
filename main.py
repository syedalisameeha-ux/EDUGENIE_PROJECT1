import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from explanation_module import explain_topic
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

app = FastAPI(
    title="EduGenie API",
    description="A Gemini-powered learning assistant for explanations, Q&A, quizzes, summaries, and learning paths.",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

Task = Literal["explain", "qa", "quiz", "summarize", "learn"]


class TaskRequest(BaseModel):
    task: Task
    text: str = Field(min_length=2, max_length=20000)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "ok", "app": "EduGenie"}


@app.post("/qa")
async def qa(payload: TaskRequest):
    return await _run("qa", payload.text)


@app.post("/explain")
async def explain(payload: TaskRequest):
    return await _run("explain", payload.text)


@app.post("/quiz")
async def quiz(payload: TaskRequest):
    return await _run("quiz", payload.text)


@app.post("/summarize")
async def summarize(payload: TaskRequest):
    return await _run("summarize", payload.text)


@app.post("/learn/recommendations")
async def learn(payload: TaskRequest):
    return await _run("learn", payload.text)


@app.post("/api/task")
async def run_task(payload: TaskRequest):
    return await _run(payload.task, payload.text)


async def _run(task: str, text: str):
    try:
        if task == "qa":
            result = await answer_question(text)
        elif task == "explain":
            result = await explain_topic(text)
        elif task == "quiz":
            result = await generate_quiz(text)
        elif task == "summarize":
            result = await summarize_text(text)
        elif task == "learn":
            result = await get_learning_recommendations(text)
        else:
            raise HTTPException(status_code=400, detail="Unsupported task.")
        return {"task": task, "result": result}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        # Avoid exposing API keys or raw provider internals to the browser.
        print(f"EduGenie error ({task}): {type(exc).__name__}: {exc}")
        raise HTTPException(
            status_code=502,
            detail="The AI service could not complete this request. Check your API key, model availability, and network connection, then try again.",
        ) from exc


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", "8000")), reload=os.getenv("RELOAD", "true").lower() == "true")
