from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_rejects_short_input():
    response = client.post("/api/task", json={"task": "qa", "text": "x"})
    assert response.status_code == 422


def test_unknown_task_rejected():
    response = client.post("/api/task", json={"task": "translate", "text": "Hello there"})
    assert response.status_code == 422


def test_task_calls_module(monkeypatch):
    async def fake_answer(text):
        return "Mock answer"
    monkeypatch.setattr(main, "answer_question", fake_answer)
    response = client.post("/api/task", json={"task": "qa", "text": "What is AI?"})
    assert response.status_code == 200
    assert response.json() == {"task": "qa", "result": "Mock answer"}
