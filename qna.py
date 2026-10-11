from ai_client import generate_text


async def answer_question(question: str) -> str:
    question = question.strip()
    if len(question) < 2:
        raise ValueError("Please enter a question.")
    return generate_text(
        "You are EduGenie, a helpful academic tutor. Answer the student's question clearly and concisely. "
        "If the question is ambiguous, state your assumption. If uncertain, say so rather than inventing facts.\n\n"
        f"Student question: {question}"
    )
