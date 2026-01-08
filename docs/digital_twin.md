# Digital Twin (MVP)

The Digital Twin stores a per-user profile and memories that the assistant can consult for personalization.

Key fields:
- user_id, name, preferences
- emotion_history: time-series of detected emotions
- long_term_memory: key/value items (reminders, preferences discovered from chat)
- behavior: derived statistics (counts, frequent intents)

Why it matters:
- Drives personalized responses (e.g., upbeat tone for positive users)
- Enables prediction and proactive suggestions
- Supports continuous learning and long-term adaptation

Exam points:
- Explain how emotion_history is stored and how decay or time-weighting would work
- Describe privacy implications and options (local storage, encryption, user controls)
