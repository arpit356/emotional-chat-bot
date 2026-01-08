from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import database

router = APIRouter()

class PreferenceIn(BaseModel):
    key: str
    value: str

@router.get("/user/{user_id}")
async def get_user(user_id: str):
    twin = database.get_user_twin(user_id)
    if not twin:
        raise HTTPException(status_code=404, detail="User not found")
    return twin

@router.get("/user/{user_id}/twin")
async def get_enriched_twin(user_id: str):
    from app.services.twin_manager import build_twin
    twin = build_twin(user_id)
    if not twin:
        raise HTTPException(status_code=404, detail="User not found")
    # Convert dataclass to dict for response
    from dataclasses import asdict
    return asdict(twin)

@router.post("/user/{user_id}/update_preference")
async def update_preference(user_id: str, pref: PreferenceIn):
    # For MVP we store preferences as a JSON-encoded string in users table (simple)
    twin = database.get_user_twin(user_id)
    if not twin:
        raise HTTPException(status_code=404, detail="User not found")
    # Very simple approach: append/update preference by rebuilding string
    # In production, preferences should be a proper JSON field / separate table
    import json
    prefs = {}
    try:
        prefs = json.loads(twin.get('preferences') or '{}')
    except Exception:
        prefs = {}
    prefs[pref.key] = pref.value
    conn = database._get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE users SET preferences = ? WHERE user_id = ?", (json.dumps(prefs), user_id))
    conn.commit()
    conn.close()
    return {"status": "ok", "preferences": prefs}

@router.get("/user/{user_id}/emotions")
async def get_emotion_history(user_id: str, limit: int = 20):
    conn = database._get_conn()
    cur = conn.cursor()
    cur.execute("SELECT ts, emotion, confidence, modality, text_sample FROM emotions WHERE user_id = ? ORDER BY ts DESC LIMIT ?", (user_id, limit))
    rows = cur.fetchall()
    conn.close()
    results = []
    for r in rows:
        results.append({"ts": r[0], "emotion": r[1], "confidence": r[2], "modality": r[3], "text": r[4]})
    return {"user_id": user_id, "emotions": results}

@router.get("/user/{user_id}/memories")
async def get_memories(user_id: str):
    mems = database.get_memories(user_id)
    return {"user_id": user_id, "memories": mems}
