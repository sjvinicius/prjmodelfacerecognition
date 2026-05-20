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
            "event_id": event_data.get(
                "event_id"
            ),
            "event_type": event_data.get(
                "event_type"
            ),
            "timestamp": event_data.get(
                "timestamp"
            ),
            "camera_id": payload.get(
                "camera_id"
            ),
            "person_id": payload.get(
                "person_id"
            ),
            "confidence": payload.get(
                "confidence"
            ),
            "snapshot_path": payload.get(
                "snapshot_path"
            )
        }

        (
            self.supabase_client.client
            .table("access_logs")
            .insert(insert_data)
            .execute()
        )

        logger.info(
            f"Event "
            f"'{event_data['event_id']}' "
            f"saved successfully"
        )


event_repository = EventRepository()