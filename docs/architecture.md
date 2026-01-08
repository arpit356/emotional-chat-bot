# Architecture Overview

MVP architecture:
- Frontend: static HTML/JS chat that posts to `/api/v1/message`
- Backend: FastAPI app handling messages, simple emotion & intent services
- Storage: SQLite database storing users and emotion history

Data flow:
User -> Frontend -> Backend (/message) -> Emotion/Intent -> Decision -> Update Twin -> Response

Next steps:
- Add STT (Whisper) and TTS (Coqui) services
- Replace keyword detectors with fine-tuned models
- Add context manager, session store, and more detailed twin schema
