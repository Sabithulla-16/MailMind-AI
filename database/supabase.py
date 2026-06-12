from supabase import create_client
from utils.config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

def test_connection():
    try:
        response = (
            supabase.table("users")
            .select("*")
            .limit(1)
            .execute()
        )

        return {
            "success": True,
            "message": "Supabase Connected"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }