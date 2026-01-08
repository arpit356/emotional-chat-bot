# Emotion-Aware Digital Twin Assistant (MVP)

This repository contains an MVP implementation of an emotion-aware virtual assistant that builds a simple Digital Twin and responds to user messages with emotion-aware replies.

## Quick start
1. Create a virtual environment:
   - `python -m venv venv` and activate it (`venv\Scripts\activate` on Windows)
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Run the backend:
   - `uvicorn backend.app.main:app --reload --port 8000`
4. Open `frontend/public/index.html` in your browser (or serve it with a simple static server).

## What is included
- FastAPI backend with `/api/v1/message` endpoint
- Simple keyword-based emotion and intent detectors
- SQLite storage for user twin, emotion history, and memories
- Minimal frontend chat UI

API endpoints (MVP):
- POST /api/v1/message -> send text message and get emotion-aware response
- GET /api/v1/user/{user_id} -> basic user record
- GET /api/v1/user/{user_id}/twin -> enriched Digital Twin (emotion history, memories)
- GET /api/v1/user/{user_id}/memories -> list stored memories (e.g., reminders)

This is intended as a starting point; follow the docs to extend modules (STT/TTS, ML-based detectors, decision engine, avatar, etc.).

Optional STT/TTS setup:
- For TTS (gTTS) the dependency is already listed; no extra OS steps required.
- For local Whisper STT you must install `openai-whisper` and `ffmpeg`:
  - `pip install -U openai-whisper`
  - On Windows, install `ffmpeg` and add it to your PATH (see https://ffmpeg.org/)
- If you want offline TTS via Coqui TTS install `TTS` (may require more setup).

Behavior notes:
- The frontend supports recording audio (hold the 🎙️ button), sends audio to the backend, receives a text response and optional TTS audio base64, and plays the audio.
- If Whisper or gTTS are not installed, the server will respond but without TTS/STT functionality (it will return helpful error messages).
