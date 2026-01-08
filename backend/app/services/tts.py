"""Text-to-Speech utilities (MVP)

- synthesize_text_to_mp3_base64: returns base64-encoded mp3 bytes (gTTS)
- If gTTS is not available this function raises an informative error.
"""
import base64
import io
from typing import Dict

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except Exception:
    GTTS_AVAILABLE = False


def synthesize_text_to_mp3_base64(text: str, lang: str = "en") -> Dict:
    """Return {'audio_base64': str, 'format': 'mp3'}"""
    if not GTTS_AVAILABLE:
        raise RuntimeError("gTTS not available. Install gTTS or configure Coqui TTS for offline TTS.")
    buf = io.BytesIO()
    tts = gTTS(text, lang=lang)
    tts.write_to_fp(buf)
    buf.seek(0)
    b = buf.read()
    return {"audio_base64": base64.b64encode(b).decode('utf-8'), "format": "mp3"}
