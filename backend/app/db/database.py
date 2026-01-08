import sqlite3
import time
from typing import Optional, Dict

DB_PATH = "digital_twin.db"


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _get_conn()
    cur = conn.cursor()
    # users table stores basic twin info as JSON (string) for MVP
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        name TEXT,
        preferences TEXT,
        created_at REAL
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS emotions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        ts REAL,
        emotion TEXT,
        confidence REAL,
        modality TEXT,
        text_sample TEXT
    )
    ''')
    # memories table: store simple key-value long-term memories for the twin
    cur.execute('''
    CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        key TEXT,
        value TEXT,
        last_seen REAL
    )
    ''')
    conn.commit()
    conn.close()


def ensure_user_exists(user_id: str, name: Optional[str] = None):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
    if not cur.fetchone():
        cur.execute("INSERT INTO users (user_id, name, preferences, created_at) VALUES (?, ?, ?, ?)",
                    (user_id, name or "", "{}", time.time()))
        conn.commit()
    conn.close()


def get_user_twin(user_id: str) -> Optional[Dict]:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT user_id, name, preferences, created_at FROM users WHERE user_id = ?", (user_id,))
    r = cur.fetchone()
    conn.close()
    if not r:
        return None
    return {"user_id": r["user_id"], "name": r["name"], "preferences": r["preferences"], "created_at": r["created_at"]}


def update_twin(user_id: str, emotion: dict, text_sample: str = None):
    # store emotion to history table and optionally update simple fields
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO emotions (user_id, ts, emotion, confidence, modality, text_sample) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, time.time(), emotion.get("label"), float(emotion.get("confidence", 0.0)), emotion.get("source"), text_sample),
    )
    conn.commit()
    conn.close()


def add_memory(user_id: str, key: str, value: str):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO memories (user_id, key, value, last_seen) VALUES (?, ?, ?, ?)",
        (user_id, key, value, time.time()),
    )
    conn.commit()
    conn.close()


def get_memories(user_id: str):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT key, value, last_seen FROM memories WHERE user_id = ? ORDER BY last_seen DESC", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [{"key": r[0], "value": r[1], "last_seen": r[2]} for r in rows]
