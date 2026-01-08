from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import messaging, user, streaming
from app.db import database

app = FastAPI(title="Emotion-Aware Digital Twin Assistant (MVP)")

# Allow local frontend to call backend during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(messaging.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(streaming.router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    # Initialize DB and create sample user
    database.init_db()
    database.ensure_user_exists("u1")

@app.get("/")
async def read_root():
    return {"status": "ok", "message": "Emotion-Aware Digital Twin Assistant API"}
