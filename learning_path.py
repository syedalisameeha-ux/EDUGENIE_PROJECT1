from ai_client import generate_text


async def get_learning_recommendations(topic: str) -> str:
    topic = topic.strip()
    if len(topic) < 2:
        raise ValueError("Please enter a topic for your learning path.")
    return generate_text(
        "You are an educational learning coach. Create a practical learning path for this topic. "
        "Organize it from beginner to intermediate to advanced, include a suggested timeline, practice activities, "
        "and types of resources to search for (official docs, tutorials, videos, books). Do not invent specific URLs. "
        "Finish with a small first task the learner can do today.\n\n"
        f"Topic: {topic}"
    )
