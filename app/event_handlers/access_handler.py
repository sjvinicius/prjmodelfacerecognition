from app.core.logger import logger

from app.infrastructure.messaging.event_bus import (
    event_bus
)

from app.services.event_queue_service import (
    event_queue_service
)

from app.services.snapshot_service import (
    snapshot_service
)

from app.services.camera_service import (
    camera_service
)


class AccessHandler:

    def __init__(self):

        event_bus.subscribe(
            "ACCESS_GRANTED",
            self.on_access_granted
        )

        event_bus.subscribe(
            "ACCESS_DENIED",
            self.on_access_denied
        )

    def on_access_granted(
        self,
        payload: dict
    ) -> None:

        logger.info(
            f"[ACCESS_GRANTED] "
            f"Person '{payload['person_id']}' "
            f"recognized on camera "
            f"'{payload['camera_id']}'"
        )

        snapshot_path = self._save_snapshot(
            payload["camera_id"],
            prefix="access_granted"
        )

        event_payload = {
            "camera_id": payload["camera_id"],
            "person_id": payload["person_id"],
            "confidence": payload["confidence"],
            "snapshot_path": snapshot_path
        }

        event_queue_service.enqueue(
            event_type="ACCESS_GRANTED",
            payload=event_payload
        )

    def on_access_denied(
        self,
        payload: dict
    ) -> None:

        logger.warning(
            f"[ACCESS_DENIED] "
            f"Unknown person detected "
            f"on camera '{payload['camera_id']}'"
        )

        snapshot_path = self._save_snapshot(
            payload["camera_id"],
            prefix="access_denied"
        )

        event_payload = {
            "camera_id": payload["camera_id"],
            "snapshot_path": snapshot_path
        }

        event_queue_service.enqueue(
            event_type="ACCESS_DENIED",
            payload=event_payload
        )

    def _save_snapshot(
        self,
        camera_id: str,
        prefix: str
    ) -> str | None:

        try:

            frame = camera_service.get_frame(
                camera_id
            )

            if frame is None:
                return None

            snapshot_path = (
                snapshot_service.save_snapshot(
                    image=frame.image,
                    prefix=prefix
                )
            )

            return snapshot_path

        except Exception as error:

            logger.error(
                f"Failed to save snapshot: "
                f"{error}"
            )

            return None


access_handler = AccessHandler()