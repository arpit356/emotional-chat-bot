"""Speech-to-Text utilities (MVP)

- transcribe_audio_base64: accepts base64-encoded audio bytes and returns transcript.
- Implementation tries to use OpenAI Whisper if available. Otherwise raises informative error.
"""
import base64
import tempfile
import os
import io

from typing import Dict

try:
    import whisper
    WHISPER_AVAILABLE = True
except Exception:
    WHISPER_AVAILABLE = False

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except Exception:
    PYDUB_AVAILABLE = False

# Load model lazily and reuse to avoid repeated loads
_MODEL = None

def _get_model():
    global _MODEL
    if _MODEL is None and WHISPER_AVAILABLE:
        _MODEL = whisper.load_model("base")
    return _MODEL


def _write_temp_file(binary: bytes, suffix: str = ".wav") -> str:
    fd, path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    with open(path, "wb") as f:
        f.write(binary)
    return path


def transcribe_audio_bytes(audio_bytes: bytes) -> Dict:
    """Transcribe raw audio bytes using available provider."""
    tmp_in = _write_temp_file(audio_bytes, suffix=".input")
    tmp_path = tmp_in

    if PYDUB_AVAILABLE:
        try:
            seg = AudioSegment.from_file(io.BytesIO(audio_bytes))
            tmp_wav = _write_temp_file(b"", suffix=".wav")
            seg.export(tmp_wav, format="wav")
            tmp_path = tmp_wav
        except Exception:
            tmp_path = tmp_in

    if WHISPER_AVAILABLE:
        model = _get_model()
        try:
            result = model.transcribe(tmp_path)
            text = result.get("text", "").strip()
            return {"text": text, "provider": "whisper_local", "confidence": 0.9}
        finally:
            try:
                os.remove(tmp_in)
            except Exception:
                pass
            if tmp_path != tmp_in:
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
    else:
        try:
            os.remove(tmp_in)
        except Exception:
            pass
        raise RuntimeError("STT provider not available. Install 'openai-whisper' and 'ffmpeg' or provide an external STT service.")


def transcribe_audio_base64(audio_b64: str) -> Dict:
    """Decode base64 audio and return transcription dict {text, provider, confidence} by delegating to bytes method."""
    if not audio_b64:
        return {"text": "", "provider": "none", "confidence": 0.0}
    audio_bytes = base64.b64decode(audio_b64)
    return transcribe_audio_bytes(audio_bytes)
