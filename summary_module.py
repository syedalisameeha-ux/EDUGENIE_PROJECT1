from ai_client import generate_text


async def summarize_text(text: str) -> str:
    text = text.strip()
    if len(text) < 20:
        raise ValueError("Please enter a longer passage (at least 20 characters) to summarize.")
    return generate_text(
        "Summarize the educational passage below in clear, simple language. Preserve the main ideas and important facts. "
        "Use a short paragraph followed by key points when useful. Do not add facts that are not in the passage.\n\n"
        f"Passage:\n{text}"
    )
