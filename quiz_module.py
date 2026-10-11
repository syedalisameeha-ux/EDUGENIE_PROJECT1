import json
from ai_client import generate_text


def _remove_markdown_fence(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text


async def generate_quiz(source: str) -> list[dict]:
    source = source.strip()
    if len(source) < 10:
        raise ValueError("For a useful quiz, enter a topic or passage of at least 10 characters.")
    prompt = f"""
Create exactly 3 educational multiple-choice questions based on the topic/passage below.
Return only a JSON array. Each item must have:
- "question": string
- "options": an array of exactly 4 strings
- "answer": the exact correct option string
- "explanation": a brief explanation
Do not include markdown fences. Ensure every answer is present in options.

Topic/passage:
{source}
"""
    raw = _remove_markdown_fence(generate_text(prompt, json_mode=True))
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("The AI returned quiz data that was not valid JSON. Please try again.") from exc
    if not isinstance(data, list) or len(data) != 3:
        raise RuntimeError("The AI did not return exactly three quiz questions. Please try again.")
    cleaned = []
    for item in data:
        if not isinstance(item, dict):
            raise RuntimeError("The AI returned an invalid quiz question.")
        question = str(item.get("question", "")).strip()
        options = item.get("options", [])
        answer = str(item.get("answer", "")).strip()
        explanation = str(item.get("explanation", "")).strip()
        if not question or not isinstance(options, list) or len(options) != 4:
            raise RuntimeError("A quiz question was missing its question or four options.")
        options = [str(option).strip() for option in options]
        if answer not in options:
            raise RuntimeError("A quiz answer did not match one of its four options.")
        cleaned.append({"question": question, "options": options, "answer": answer, "explanation": explanation})
    return cleaned
