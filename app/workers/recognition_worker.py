import threading
import time

from app.core.config import settings
from app.core.logger import logger

from app.services.camera_service import (
    camera_service
)

from app.services.recognition_service import (
    recognition_service
)

from app.infrastructure.messaging.event_bus import (
    event_bus
)


class RecognitionWorker:

    def __init__(self):

        self._thread = None

        self._running = False

    def start(self) -> None:

        if self._running:

            logger.warning(
                "Recognition worker already running"
            )

            return

        self._running = True

        self._thread = threading.Thread(
            target=self._run,
            daemon=True
        )

        self._thread.start()

        logger.info(
            "Recognition worker started"
        )

    def stop(self) -> None:

        self._running = False

        logger.info(
            "Recognition worker stopped"
        )

    def _run(self) -> None:

        while self._running:

            try:

                cameras = (
                    camera_service.list_cameras()
                )

                for camera_id in cameras:

                    try:

                        result = (
                            recognition_service
                            .process_camera(camera_id)
                        )

                        logger.info(
                            f"Recognition result: "
                            f"{result}"
                        )

                        for recognition in result["results"]:

                            match = recognition["match"]

                            if match["matched"]:

                                event_bus.publish(
                                    "FACE_RECOGNIZED",
                                    {
                                        "camera_id": camera_id,
                                        "person_id": match["person_id"],
                                        "confidence": match["confidence"]
                                    }
                                )

                                event_bus.publish(
                                    "ACCESS_GRANTED",
                                    {
                                        "camera_id": camera_id,
                                        "person_id": match["person_id"],
                                        "confidence": match["confidence"]
                                    }
                                )

                            else:

                                event_bus.publish(
                                    "UNKNOWN_PERSON",
                                    {
                                        "camera_id": camera_id
                                    }
                                )

                                event_bus.publish(
                                    "ACCESS_DENIED",
                                    {
                                        "camera_id": camera_id
                                    }
                                )

                    except Exception as error:

                        logger.error(
                            f"Recognition error "
                            f"for '{camera_id}': "
                            f"{error}"
                        )

            except Exception as error:

                logger.error(
                    f"Recognition worker failure: "
                    f"{error}"
                )

            time.sleep(
                settings.RECOGNITION_INTERVAL
            )


recognition_worker = RecognitionWorker()