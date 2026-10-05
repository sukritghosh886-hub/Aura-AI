from app.services.supabase import get_admin_client


def save_memory(
    user_id: str,
    content: str,
    memory_type: str = "general",
    importance: int = 1
):
    supabase = get_admin_client()

    return supabase.table("memories").insert({
        "user_id": user_id,
        "content": content,
        "memory_type": memory_type,
        "importance": importance
    }).execute()


def get_memories(user_id: str, limit: int = 20):
    supabase = get_admin_client()

    result = (
        supabase
        .table("memories")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return result.data or []