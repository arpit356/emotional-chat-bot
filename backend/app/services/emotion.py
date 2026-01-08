from typing import Dict

# Simple keyword-based emotion detector for MVP
# We also provide basic valence/arousal estimates to help the decision engine
EMOTION_METADATA = {
    "happy": {"valence": 0.9, "arousal": 0.7},
    "sad": {"valence": -0.8, "arousal": 0.3},
    "angry": {"valence": -0.7, "arousal": 0.9},
    "neutral": {"valence": 0.0, "arousal": 0.4}
}

EMOTION_KEYWORDS = {
    "happy": ["happy", "glad", "great", "awesome", "excited", "joy", "nice", "content", "pleased", "joyful"],
    "sad": ["sad", "unhappy", "down", "depressed", "upset", "cry", "crying", "tears", "miserable", "lonely"],
    "angry": ["angry", "mad", "furious", "annoyed", "frustrat"],
}


def detect_emotion(text: str) -> Dict:
    """Return an emotion dict with label, confidence, source, valence, arousal.

    This function is intentionally simple to keep the MVP accessible. Replace
    with a model-based detector later (transformers, fine-tuned classifier).
    """
    txt = (text or "").lower()
    for emo, keywords in EMOTION_KEYWORDS.items():
        for k in keywords:
            if k in txt:
                meta = EMOTION_METADATA.get(emo, EMOTION_METADATA['neutral'])
                return {"label": emo, "confidence": 0.9, "source": "keywords", "valence": meta['valence'], "arousal": meta['arousal']}
    # fallback to neutral
    meta = EMOTION_METADATA['neutral']
    return {"label": "neutral", "confidence": 0.6, "source": "fallback", "valence": meta['valence'], "arousal": meta['arousal']}


def get_emotion_vector(emotion: Dict) -> Dict:
    """Return numeric vector (valence, arousal) for downstream modules."""
    return {"valence": emotion.get('valence', 0.0), "arousal": emotion.get('arousal', 0.0)}
