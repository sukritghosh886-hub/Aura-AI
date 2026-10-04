import os
from typing import Optional

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from supabase import create_client, Client


app = FastAPI(
    title="Aura AI",
    version="0.3.0",
)


# ==================================================
# SUPABASE
# ==================================================

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY")

supabase: Optional[Client] = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(
            SUPABASE_URL,
            SUPABASE_KEY,
        )
    except Exception:
        supabase = None


# ==================================================
# REQUEST / RESPONSE MODELS
# ==================================================

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"


class ChatResponse(BaseModel):
    reply: str
    session_id: str


# ==================================================
# HEALTH
# ==================================================

@app.get("/api/health")
async def health():

    return {
        "status": "ok",
        "service": "Aura AI",
        "version": "0.3.0",
        "database": "configured" if supabase else "not_configured",
        "ai_engine": "Aura Model Adapter",
    }


# ==================================================
# AURA MODEL ENGINE
# ==================================================

async def call_model(message: str) -> str:
    """
    Aura's model adapter.

    The model server can later be our own
    open-weight AI model.

    No external AI API key is required
    for this adapter to exist.
    """

    model_url = os.getenv("AURA_MODEL_URL")

    # ----------------------------------------------
    # Our own model API
    # ----------------------------------------------

    if model_url:

        payload = {
            "message": message,
            "model": os.getenv(
                "AURA_MODEL_NAME",
                "aura-model",
            ),
        }

        async with httpx.AsyncClient(timeout=120) as client:

            response = await client.post(
                model_url,
                json=payload,
            )

        if response.status_code >= 400:

            raise HTTPException(
                status_code=502,
                detail="Aura model server request failed",
            )

        data = response.json()

        return data.get(
            "reply",
            "The Aura model returned no reply.",
        )

    # ----------------------------------------------
    # Development fallback
    # ----------------------------------------------

    text = message.lower().strip()

    if text in {"hello", "hi", "hey"}:

        return (
            "Hello. I am Aura AI. "
            "My own model engine is being built."
        )

    if "who are you" in text:

        return (
            "I am Aura AI, a modular personal AI system. "
            "My model layer is designed to use an "
            "open-weight model that we control."
        )

    if "status" in text:

        return (
            "Aura backend is running. "
            "The external model server is not connected yet."
        )

    return (
        "Aura received your message. "
        "The Aura model server is not connected yet. "
        "The next stage is to connect our open-weight model."
    )


# ==================================================
# CHAT
# ==================================================

@app.post(
    "/api/chat",
    response_model=ChatResponse,
)
async def chat(request: ChatRequest):

    message = request.message.strip()

    if not message:

        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty",
        )

    session_id = request.session_id or "default"

    conversation_id = None

    # ----------------------------------------------
    # SUPABASE STORAGE
    # ----------------------------------------------

    if supabase:

        try:

            conversation = (
                supabase
                .table("conversations")
                .select("id")
                .eq("title", session_id)
                .limit(1)
                .execute()
            )

            if conversation.data:

                conversation_id = conversation.data[0]["id"]

            else:

                created = (
                    supabase
                    .table("conversations")
                    .insert({
                        "title": session_id
                    })
                    .execute()
                )

                if created.data:

                    conversation_id = created.data[0]["id"]

            if conversation_id:

                supabase.table("messages").insert({
                    "conversation_id": conversation_id,
                    "role": "user",
                    "content": message,
                }).execute()

        except Exception:

            conversation_id = None

    # ----------------------------------------------
    # AURA MODEL
    # ----------------------------------------------

    reply = await call_model(message)

    # ----------------------------------------------
    # SAVE AURA RESPONSE
    # ----------------------------------------------

    if supabase and conversation_id:

        try:

            supabase.table("messages").insert({
                "conversation_id": conversation_id,
                "role": "assistant",
                "content": reply,
            }).execute()

        except Exception:

            pass

    return ChatResponse(
        reply=reply,
        session_id=session_id,
    )


# ==================================================
# FRONTEND
# ==================================================

app.mount(
    "/",
    StaticFiles(
        directory="web",
        html=True,
    ),
    name="web",
)
