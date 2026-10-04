import os
from typing import Optional

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from supabase import create_client, Client


app = FastAPI(
    title="Aura AI",
    version="0.2.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Supabase
# --------------------------------------------------

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY")

supabase: Optional[Client] = None

if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(
        SUPABASE_URL,
        SUPABASE_KEY,
    )


# --------------------------------------------------
# Models
# --------------------------------------------------

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"


class ChatResponse(BaseModel):
    reply: str
    session_id: str


# --------------------------------------------------
# Health
# --------------------------------------------------

@app.get("/api/health")
async def health():

    return {
        "status": "ok",
        "service": "Aura AI",
        "version": "0.2.0",
        "database": "connected" if supabase else "not_configured",
    }


# --------------------------------------------------
# AI model
# --------------------------------------------------

async def call_model(message: str) -> str:

    api_key = os.getenv("AI_API_KEY")

    if not api_key:

        return (
            "Aura is running, but no AI_API_KEY is configured yet."
        )

    base_url = os.getenv(
        "AI_BASE_URL",
        "https://api.openai.com/v1",
    )

    model = os.getenv(
        "AI_MODEL",
        "gpt-5.6-mini",
    )

    payload = {

        "model": model,

        "messages": [

            {
                "role": "system",
                "content": (
                    "You are Aura AI, a helpful personal AI assistant. "
                    "Be concise, useful, and honest. "
                    "Never claim an action was performed unless it actually was."
                ),
            },

            {
                "role": "user",
                "content": message,
            },

        ],

        "temperature": 0.2,
    }

    headers = {

        "Authorization": f"Bearer {api_key}",

        "Content-Type": "application/json",

    }

    async with httpx.AsyncClient(timeout=60) as client:

        response = await client.post(

            f"{base_url.rstrip('/')}/chat/completions",

            json=payload,

            headers=headers,

        )

    if response.status_code >= 400:

        raise HTTPException(
            status_code=502,
            detail="AI provider request failed",
        )

    data = response.json()

    return data["choices"][0]["message"]["content"]


# --------------------------------------------------
# Chat
# --------------------------------------------------

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

    # ----------------------------------------------
    # Save user message
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

                conversation_id = created.data[0]["id"]

            supabase.table("messages").insert({

                "conversation_id": conversation_id,
                "role": "user",
                "content": message,

            }).execute()

        except Exception:

            # Database failure must not crash Aura's chat.
            conversation_id = None

    else:

        conversation_id = None


    # ----------------------------------------------
    # Generate Aura response
    # ----------------------------------------------

    reply = await call_model(message)


    # ----------------------------------------------
    # Save Aura response
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


# --------------------------------------------------
# Web interface
# --------------------------------------------------

app.mount(

    "/",

    StaticFiles(
        directory="web",
        html=True,
    ),

    name="web",

)