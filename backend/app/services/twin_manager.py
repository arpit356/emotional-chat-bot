from app.models.twin import UserTwin, LongTermMemoryItem
from app.db import database
import time


def build_twin(user_id: str) -> UserTwin:
    raw = database.get_user_twin(user_id)
    if not raw:
        return None
    # build emotion summary (last N)
    conn = database._get_conn()
    cur = conn.cursor()
    cur.execute("SELECT ts, emotion, confidence, text_sample FROM emotions WHERE user_id = ? ORDER BY ts DESC LIMIT 50", (user_id,))
    rows = cur.fetchall()
    emotions = []
    for r in rows:
        emotions.append({"ts": r[0], "emotion": r[1], "confidence": r[2], "text": r[3]})
    conn.close()

    mems_raw = database.get_memories(user_id)
    ltm = [LongTermMemoryItem(key=m['key'], value=m['value'], last_seen=m['last_seen']) for m in mems_raw]

    twin = UserTwin(
        user_id=user_id,
        name=raw.get('name'),
        preferences=raw.get('preferences') and __safe_parse(raw.get('preferences')) or {},
        emotion_history=emotions,
        long_term_memory=ltm,
        session_memory={}
    )
    # compute simple behavior metrics
    twin.behavior = _compute_behavior(emotions)
    return twin


def _compute_behavior(emotions):
    # Very simple stats: count emotions
    counts = {}
    for e in emotions:
        label = e.get('emotion') or 'unknown'
        counts[label] = counts.get(label, 0) + 1
    return {"emotion_counts": counts, "total_interactions": sum(counts.values())}


def __safe_parse(s):
    import json
    try:
        return json.loads(s)
    except Exception:
        return {}
