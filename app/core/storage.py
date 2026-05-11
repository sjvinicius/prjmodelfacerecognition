from pathlib import Path

from app.core.logger import logger


class Storage:

    def __init__(self):

        self.base_path = Path("storage")

        self.queue_path = (
            self.base_path / "queue"
        )

        self.pending_queue_path = (
            self.queue_path / "pending"
        )

        self.processing_queue_path = (
            self.queue_path / "processing"
        )

        self.failed_queue_path = (
            self.queue_path / "failed"
        )

        self.completed_queue_path = (
            self.queue_path / "completed"
        )

        self.snapshots_path = (
            self.base_path / "snapshots"
        )

        self.temp_path = (
            self.base_path / "temp"
        )

        self._create_directories()

    def _create_directories(self) -> None:

        directories = [
            self.base_path,
            self.queue_path,
            self.pending_queue_path,
            self.processing_queue_path,
            self.failed_queue_path,
            self.completed_queue_path,
            self.snapshots_path,
            self.temp_path
        ]

        for directory in directories:

            directory.mkdir(
                parents=True,
                exist_ok=True
            )

            logger.info(
                f"Storage directory ready: "
                f"{directory}"
            )


storage = Storage()