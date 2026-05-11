import json

from datetime import datetime
from pathlib import Path
from uuid import uuid4

from app.core.logger import logger
from app.core.storage import storage


class EventQueueService:

    def enqueue(
        self,
        event_type: str,
        payload: dict
    ) -> str:

        event_id = uuid4().hex

        timestamp = datetime.utcnow().isoformat()

        event_data = {
            "event_id": event_id,
            "event_type": event_type,
            "timestamp": timestamp,
            "payload": payload
        }

        filename = (
            f"{timestamp}_{event_id}.json"
        )

        filename = filename.replace(
            ":",
            "-"
        )

        event_path = (
            storage.pending_queue_path
            / filename
        )

        with open(
            event_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                event_data,
                file,
                ensure_ascii=False,
                indent=4
            )

        logger.info(
            f"Event queued: '{event_type}' "
            f"-> {event_path}"
        )

        return str(event_path)

    def list_pending_events(
        self
    ) -> list[Path]:

        events = list(
            storage.pending_queue_path.glob(
                "*.json"
            )
        )

        events.sort()

        return events

    def move_to_processing(
        self,
        event_path: Path
    ) -> Path:

        destination = (
            storage.processing_queue_path
            / event_path.name
        )

        event_path.rename(destination)

        logger.info(
            f"Event moved to processing: "
            f"{destination}"
        )

        return destination

    def move_to_completed(
        self,
        event_path: Path
    ) -> Path:

        destination = (
            storage.completed_queue_path
            / event_path.name
        )

        event_path.rename(destination)

        logger.info(
            f"Event completed: "
            f"{destination}"
        )

        return destination

    def move_to_failed(
        self,
        event_path: Path
    ) -> Path:

        destination = (
            storage.failed_queue_path
            / event_path.name
        )

        event_path.rename(destination)

        logger.warning(
            f"Event failed: "
            f"{destination}"
        )

        return destination

    def load_event(
        self,
        event_path: Path
    ) -> dict:

        with open(
            event_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


event_queue_service = EventQueueService()