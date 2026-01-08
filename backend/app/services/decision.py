def choose_response(intent: dict, emotion: dict, twin: dict) -> str:
    """Placeholder decision engine: combine signals to pick a reply.

    Replace with a more sophisticated engine (rule-based + ML) later.
    """
    # High-priority: explicit sad emotion gets empathetic reply
    if emotion.get("label") == "sad":
        if intent.get("intent") == "ask_suggestion":
            return ("I'm sorry you're feeling down. Here are a few things that sometimes help: take a short walk, "
                    "call a supportive friend, try a short breathing exercise, or write down what's on your mind. "
                    "Would you like one suggestion I can walk you through?")
        return "I'm sorry to hear that. Would you like to talk about what's bothering you?"

    # If the user explicitly asks for suggestions (and isn't sad), provide ideas
    if intent.get("intent") == "ask_suggestion":
        return ("Here are some ideas to feel better: go for a walk, listen to music you enjoy, try a short breathing or "
                "stretching exercise, or connect with a friend. Would you like a single suggestion I can walk you through?")

    if intent.get("intent") == "ask_weather":
        return "The weather seems fine — do you want a local forecast?"

    # default fallback
    return "Thanks for telling me that." 
