from app.core.logger import logger

from app.infrastructure.sync.supabase_client import (
    SupabaseClient
)


class EventRepository:

    def __init__(self):

        self.supabase_client = (
            SupabaseClient()
        )

    def save_event(
        self,
        event_data: dict
    ) -> None:

        logger.info(
            f"Saving event "
            f"'{event_data['event_type']}' "
            f"to Supabase"
        )

        payload = event_data.get(
            "payload",
            {}
        )

        insert_data = {
            "faceslogs_id": event_data.get(
                "event_id"
            ),
            "usuario_id": payload.get(
                "person_id"
            ),
            "tipoevento": event_data.get(
                "event_type"
            ),
            "camera": payload.get(
                "camera_id"
            ),
            "confidence": payload.get(
                "confidence"
            ),
            "foto_arquivo": payload.get(
                "snapshot_path"
            ),
            "criacao_token": payload.get(
                "camera_id"
            ),
            "criacao_data": event_data.get(
                "timestamp"
            ),
            "status": 'A'
        }

        (
            self.supabase_client.client
            .table("facerecoglogs")
            .insert(insert_data)
            .execute()
        )

        logger.info(
            f"Event "
            f"'{event_data['event_id']}' "
            f"saved successfully"
        )


event_repository = EventRepository()