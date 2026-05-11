import threading
import time

from datetime import datetime, timedelta
from pathlib import Path

from app.core.config import settings
from app.core.logger import logger
from app.core.storage import storage


class StorageCleanupWorker:

    def __init__(self):

        self._thread = None

        self._running = False

    def start(self) -> None:

        if self._running:

            logger.warning(
                "Storage cleanup worker already running"
            )

            return

        self._running = True

        self._thread = threading.Thread(
            target=self._run,
            daemon=True
        )

        self._thread.start()

        logger.info(
            "Storage cleanup worker started"
        )

    def stop(self) -> None:

        self._running = False

        logger.info(
            "Storage cleanup worker stopped"
        )

    def _run(self) -> None:

        while self._running:

            try:

                self._cleanup_completed()

                self._cleanup_failed()

                self._cleanup_snapshots()

            except Exception as error:

                logger.error(
                    f"Cleanup worker failure: "
                    f"{error}"
                )

            time.sleep(
                settings.STORAGE_CLEANUP_INTERVAL
            )

    def _cleanup_completed(self) -> None:

        self._cleanup_directory(
            directory=storage.completed_queue_path,
            retention_days=(
                settings.COMPLETED_RETENTION_DAYS
            )
        )

    def _cleanup_failed(self) -> None:

        self._cleanup_directory(
            directory=storage.failed_queue_path,
            retention_days=(
                settings.FAILED_RETENTION_DAYS
            )
        )

    def _cleanup_snapshots(self) -> None:

        self._cleanup_directory(
            directory=storage.snapshots_path,
            retention_days=(
                settings.SNAPSHOT_RETENTION_DAYS
            )
        )

    def _cleanup_directory(
        self,
        directory: Path,
        retention_days: int
    ) -> None:

        cutoff = datetime.utcnow() - timedelta(
            days=retention_days
        )

        files = directory.rglob("*")

        for file_path in files:

            if not file_path.is_file():
                continue

            modified_at = datetime.utcfromtimestamp(
                file_path.stat().st_mtime
            )

            if modified_at > cutoff:
                continue

            try:

                file_path.unlink()

                logger.info(
                    f"Deleted old file: "
                    f"{file_path}"
                )

            except Exception as error:

                logger.error(
                    f"Failed to delete "
                    f"'{file_path}': "
                    f"{error}"
                )


storage_cleanup_worker = StorageCleanupWorker()