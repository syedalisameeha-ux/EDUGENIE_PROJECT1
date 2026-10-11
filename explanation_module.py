"""Concept explanations. Gemini is the default; optional local LaMini mode is available."""
import os
from functools import lru_cache
from ai_client import generate_text


@lru_cache(maxsize=1)
def _load_local_pipeline():
    # Install requirements-local.txt and set EDU_USE_LOCAL_MODEL=true to enable.
    from transformers import pipeline
    model_name = os.getenv("LOCAL_MODEL_NAME", "MBZUAI/LaMini-Flan-T5-783M")
    return pipeline("text2text-generation", model=model_name, device=-1)


async def explain_topic(topic: str) -> str:
    topic = topic.strip()
    if len(topic) < 2:
        raise ValueError("Please enter a topic to explain.")
    if os.getenv("EDU_USE_LOCAL_MODEL", "false").lower() == "true":
        try:
            pipe = _load_local_pipeline()
            output = pipe(
                f"Explain this topic to a student in simple language with an example: {topic}",
                max_new_tokens=220,
                do_sample=False,
            )
            return output[0]["generated_text"].strip()
        except Exception as exc:
            raise RuntimeError(
                "The optional local model could not be loaded. Install requirements-local.txt, or set EDU_USE_LOCAL_MODEL=false to use Gemini."
            ) from exc
    return generate_text(
        "You are EduGenie, a patient tutor. Explain the following concept for a beginner. "
        "Use a short definition, simple steps or bullets, and one example. Be accurate and avoid jargon.\n\n"
        f"Topic or question: {topic}"
    )
