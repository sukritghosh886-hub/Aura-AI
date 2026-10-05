import httpx

from app.config import settings


async def generate_response(prompt: str) -> str:
    if not settings.ai_api_key or not settings.ai_base_url:
        return (
            "Aura is running in local orchestration mode. "
            "Configure the AI provider environment variables "
            "to enable model reasoning."
        )

    url = settings.ai_base_url.rstrip("/") + "/chat/completions"

    payload = {
        "model": settings.ai_model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Aura, an AI orchestration assistant. "
                    "Plan tasks carefully, respect permissions, "
                    "and never perform unauthorized security actions."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2
    }

    headers = {
        "Authorization": f"Bearer {settings.ai_api_key}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            url,
            json=payload,
            headers=headers
        )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]