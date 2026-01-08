from typing import Dict

# Very small in-memory session store for MVP.
# In production, use Redis or a proper session datastore.
_session_store: Dict[str, Dict] = {}


def get_session(session_id: str) -> Dict:
    return _session_store.get(session_id, {})


def update_session(session_id: str, updates: Dict):
    sess = _session_store.get(session_id, {})
    sess.update(updates)
    _session_store[session_id] = sess
    return sess


def clear_session(session_id: str):
    if session_id in _session_store:
        del _session_store[session_id]
