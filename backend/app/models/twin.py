"""Digital Twin schema (MVP) - clear, student-friendly dataclass-like structure."""
from typing import List, Dict, Optional
from dataclasses import dataclass, field

@dataclass
class LongTermMemoryItem:
    key: str
    value: str
    last_seen: float

@dataclass
class UserTwin:
    user_id: str
    name: Optional[str] = None
    timezone: Optional[str] = None
    preferences: Dict = field(default_factory=dict)
    emotion_history: List[Dict] = field(default_factory=list)
    behavior: Dict = field(default_factory=dict)
    long_term_memory: List[LongTermMemoryItem] = field(default_factory=list)
    session_memory: Dict = field(default_factory=dict)

# Example usage:
# twin = UserTwin(user_id='u1', name='Alice', preferences={'voice':'female'})
