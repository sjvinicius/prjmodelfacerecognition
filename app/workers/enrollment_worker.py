import threading
import time

from app.core.config import settings
from app.core.logger import logger

from app.services.enrollment_service import (
    enrollment_queue_service
)


class EnrollmentWorker:

    def __init__(self):

        self._thread = None

        self._running = False

    def start(self) -> None:

        if self._running:

            logger.warning(
                "Enrollment worker already running"
            )

            return

        self._running = True

        self._thread = threading.Thread(
            target=self._run,
            daemon=True
        )

        self._thread.start()

        logger.info(
            "Enrollment worker started"
        )

    def stop(self) -> None:

        self._running = False

        logger.info(
            "Enrollment worker stopped"
        )

    def _run(self) -> None:

        while self._running:

            try:

                pending_items = (
                    enrollment_queue_service
                    .list_pending()
                )

                for item in pending_items:

                    self._process_item(item)

            except Exception as error:

                logger.error(
                    f"Enrollment worker failure: "
                    f"{error}"
                )

            time.sleep(
                settings.ENROLLMENT_INTERVAL
            )

    def _process_item(
        self,
        item: dict
    ) -> None:

        queue_id = item["filaembeddingfacerecog_id"]

        try:

            enrollment_queue_service.mark_processing(
                queue_id
            )

            enrollment_queue_service.process_enrollment(
                user_id=item["usuario_id"],
                storage_path=item["storage_path"]
            )

            enrollment_queue_service.mark_completed(
                queue_id
            )

        except Exception as error:

            logger.error(
                f"Failed to process enrollment "
                f"'{queue_id}': "
                f"{error}"
            )

            enrollment_queue_service.mark_failed(
                queue_id,
                str(error)
            )


enrollment_worker = EnrollmentWorker()