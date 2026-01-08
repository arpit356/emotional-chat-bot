from fastapi import APIRouter
from pydantic import BaseModel
from app.services import emotion as emotion_svc
from app.services import intent as intent_svc
from app.services import decision as decision_svc
from app.services import context as context_svc
from app.services import stt as stt_svc
from app.services import tts as tts_svc
from app.db import database

router = APIRouter()

class MessageIn(BaseModel):
    user_id: str
    text: str = None
    audio_b64: str = None
    session_id: str = None

class MessageOut(BaseModel):
    text: str
    emotion: dict
    intent: dict
    tts_audio: str = None

@router.post("/message", response_model=MessageOut)
async def handle_message(msg: MessageIn):
    # Accept either text or audio (audio will be transcribed with STT)
    text = msg.text
    if not text and msg.audio_b64:
        # transcribe audio
        try:
            res = stt_svc.transcribe_audio_base64(msg.audio_b64)
            text = res.get('text')
        except Exception as e:
            # If STT fails, return an error message
            raise ValueError(f"STT error: {e}")

    if not text:
        raise ValueError("text or audio is required")

    # Detect emotion and intent
    emotion = emotion_svc.detect_emotion(text)
    intent = intent_svc.detect_intent(text)

    # Get user twin and make a simple personalized response
    twin = database.get_user_twin(msg.user_id)
    if not twin:
        # Create a minimal twin structure
        database.ensure_user_exists(msg.user_id)
        twin = database.get_user_twin(msg.user_id)

    # Special-case: set reminders (simple slot handling for MVP)
    if intent.get("intent") == "set_reminder" and intent.get("slots", {}).get("reminder_text"):
        reminder = intent["slots"]["reminder_text"]
        database.add_memory(msg.user_id, "reminder", reminder)
        response_text = f"Okay, I've set a reminder: '{reminder}'"
    else:
        # Use the decision engine to choose a response (combines intent + emotion + twin)
        response_text = decision_svc.choose_response(intent, emotion, twin)

    # Update session memory if provided
    if msg.session_id:
        context_svc.update_session(msg.session_id, {"last_intent": intent.get("intent"), "last_text": text})

    # Update twin with emotion history and last interaction
    database.update_twin(msg.user_id, emotion, text)

    # Generate TTS audio (if available) for the response. This keeps UI simple –
    # backend provides audio as base64 string that the frontend can play.
    tts_audio = None
    try:
        tts_res = tts_svc.synthesize_text_to_mp3_base64(response_text)
        tts_audio = tts_res.get('audio_base64')
    except Exception:
        tts_audio = None

    return {"text": response_text, "emotion": emotion, "intent": intent, "tts_audio": tts_audio}
