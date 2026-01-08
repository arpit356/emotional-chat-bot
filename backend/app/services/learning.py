from app.db import database
import time

# This module contains simple, rule-based memory consolidation functions for MVP.
# In production, these would be replaced by ML-based clustering/embedding methods.

def consolidate_memories(user_id: str, older_than_seconds: float = 30*24*3600):
    """Remove memories older than threshold (simple housekeeping)."""
    conn = database._get_conn()
    cur = conn.cursor()
    cutoff = time.time() - older_than_seconds
    cur.execute("DELETE FROM memories WHERE user_id = ? AND last_seen < ?", (user_id, cutoff))
    conn.commit()
    conn.close()

def extract_preferences_from_memories(user_id: str):
    """Extract simple preferences from memories, e.g., memory items with key 'pref_*'."""
    mems = database.get_memories(user_id)
    prefs = {}
    for m in mems:
        if m['key'].startswith('pref_'):
            k = m['key'][5:]
            prefs[k] = m['value']
    # merge into existing preferences
    if prefs:
        import json
        twin = database.get_user_twin(user_id)
        if twin:
            existing = {}
            try:
                existing = json.loads(twin.get('preferences') or '{}')
            except Exception:
                existing = {}
            existing.update(prefs)
            conn = database._get_conn()
            cur = conn.cursor()
            cur.execute("UPDATE users SET preferences = ? WHERE user_id = ?", (json.dumps(existing), user_id))
            conn.commit()
            conn.close()
    return prefs
