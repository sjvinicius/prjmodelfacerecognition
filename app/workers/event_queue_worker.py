import threading
import time

from pathlib import Path

from app.core.config import settings
from app.core.logger import logger

from app.services.event_queue_service import (
    event_queue_service
)

from app.infrastructure.sync.event_repository import (
    event_repository
)


class EventQueueWorker:

    def __init__(self):

        self._thread = None

        self._running = False

    def start(self) -> None:

        if self._running:

            logger.warning(
                "Event queue worker already running"
            )

            return

        self._running = True

        self._thread = threading.Thread(
            target=self._run,
            daemon=True
        )

        self._thread.start()

        logger.info(
            "Event queue worker started"
        )

    def stop(self) -> None:

        self._running = False

        logger.info(
            "Event queue worker stopped"
        )

    def _run(self) -> None:

        while self._running:

            try:

                pending_events = (
                    event_queue_service
                    .list_pending_events()
                )

                for pending_event in pending_events:

                    self._process_event(
                        pending_event
                    )

            except Exception as error:

                logger.error(
                    f"Queue worker failure: "
                    f"{error}"
                )

            time.sleep(
                settings.EVENT_QUEUE_INTERVAL
            )

    def _process_event(
        self,
        event_path: Path
    ) -> None:

        processing_path = None

        try:

            processing_path = (
                event_queue_service
                .move_to_processing(
                    event_path
                )
            )

            event_data = (
                event_queue_service
                .load_event(
                    processing_path
                )
            )

            event_repository.save_event(
                event_data
            )

            event_queue_service.move_to_completed(
                processing_path
            )

        except Exception as error:

            logger.error(
                f"Failed to process event "
                f"'{event_path.name}': "
                f"{error}"
            )

            if (
                processing_path
                and processing_path.exists()
            ):

                event_queue_service.move_to_failed(
                    processing_path
                )


event_queue_worker = EventQueueWorker()