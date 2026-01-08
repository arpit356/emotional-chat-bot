from typing import Dict
import re

INTENT_KEYWORDS = {
    "ask_weather": ["weather", "rain", "sunny", "temperature"],
    "set_reminder": ["remind", "reminder", "remember"],
    "ask_suggestion": ["what should i do", "suggest", "advice", "how to feel", "help me", "feel better", "what to do", "suggest me", "how can i feel"],
    "small_talk": ["hi", "hello", "how are you", "hey"],
}


def detect_intent(text: str) -> Dict:
    """Detect intent and simple slots (MVP). Returns dict with intent, confidence, source, slots."""
    txt = (text or "").lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        for k in keywords:
            if k in txt:
                slots = {}
                # Very naive slot extraction for reminders: "remind me to <action>"
                if intent == "set_reminder":
                    m = re.search(r"remind me to (.+)", txt)
                    if m:
                        slots['reminder_text'] = m.group(1)
                return {"intent": intent, "confidence": 0.85, "source": "keywords", "slots": slots}
    return {"intent": "unknown", "confidence": 0.5, "source": "fallback", "slots": {}}
