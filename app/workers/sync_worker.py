import threading
import time

from app.core.config import settings
from app.core.logger import logger

from app.services.face_sync_service import (
    face_sync_service
)


class SyncWorker:

    def __init__(self):

        self._thread = None

        self._running = False

    def start(self) -> None:

        if self._running:

            logger.warning(
                "Sync worker already running"
            )

            return

        self._running = True

        self._thread = threading.Thread(
            target=self._run,
            daemon=True
        )

        self._thread.start()

        logger.info(
            "Sync worker started"
        )

    def stop(self) -> None:

        self._running = False

        logger.info(
            "Sync worker stopped"
        )

    def _run(self) -> None:

        while self._running:

            try:

                synced = (
                    face_sync_service.sync_faces()
                )

                logger.info(
                    f"{synced} faces synchronized"
                )

            except Exception as error:

                logger.error(
                    f"Sync worker error: {error}"
                )

            time.sleep(
                settings.FACE_SYNC_INTERVAL
            )


sync_worker = SyncWorker()