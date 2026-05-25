import numpy as np

from app.core.logger import logger

from app.infrastructure.sync.supabase_client import (
    SupabaseClient
)

from app.services.recognition_service import (
    recognition_service
)


class FaceSyncService:

    def __init__(self):

        self.supabase_client = SupabaseClient()

    def sync_faces(self) -> int:

        logger.info(
            "Starting face synchronization"
        )

        faces = (
            self.supabase_client
            .fetch_authorized_faces()
        )

        synced_count = 0

        for face in faces:

            person_id = face.get("usuario_id")

            embedding = face.get("embedding")

            if not person_id or not embedding:
                continue

            try:

                embedding_array = np.array(
                    embedding,
                    dtype=np.float32
                )

                recognition_service.register_face(
                    person_id=person_id,
                    embedding=embedding_array
                )

                synced_count += 1

            except Exception as error:

                logger.error(
                    f"Failed to sync face "
                    f"'{person_id}': {error}"
                )

        logger.info(
            f"{synced_count} faces synchronized"
        )

        return synced_count


face_sync_service = FaceSyncService()