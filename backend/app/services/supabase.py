from supabase import create_client, Client

from app.config import settings


def get_user_client() -> Client:
    return create_client(
        settings.supabase_url,
        settings.supabase_publishable_key
    )


def get_admin_client() -> Client:
    if not settings.supabase_secret_key:
        raise RuntimeError("SUPABASE_SECRET_KEY is not configured.")

    return create_client(
        settings.supabase_url,
        settings.supabase_secret_key
    )