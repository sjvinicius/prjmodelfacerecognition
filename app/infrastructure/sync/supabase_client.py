from supabase import Client, create_client

from app.core.config import settings
from app.core.logger import logger


class SupabaseClient:

    def __init__(self):

        logger.info(
            "Initializing Supabase client"
        )

        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )

    def fetch_authorized_faces(
        self
    ) -> list[dict]:

        logger.info(
            "Fetching authorized faces from Supabase"
        )

        response = (
            self.client
            .table("facesautorizadas")
            .select("*")
            .execute()
        )

        data = response.data or []

        return data