import threading
import time

from app.core.config import settings
from app.core.logger import logger

from app.services.camera_service import camera_service
from app.services.recognition_service import recognition_service
from app.infrastructure.messaging.event_bus import event_bus
from app.services.camera_service import camera_service
from app.infrastructure.camera.frame import Frame


class RecognitionWorker:

    def __init__(self):
        self._thread = None
        self._running = False

        # controla frequência por câmera
        self._last_run_by_camera = {}

    def start(self) -> None:

        if self._running:
            logger.warning("Recognition worker already running")
            return

        self._running = True

        self._thread = threading.Thread(
            target=self._run,
            daemon=True
        )

        self._thread.start()

        logger.info("Recognition worker started")

    def stop(self) -> None:
        self._running = False
        logger.info("Recognition worker stopped")

    def _run(self) -> None:

        interval = settings.RECOGNITION_INTERVAL  # ex: 0.2s

        while self._running:

            try:
                cameras = camera_service.list_cameras()
                now = time.time()

                for camera_id in cameras:

                    # 🔥 throttle por câmera (evita overload)
                    last = self._last_run_by_camera.get(camera_id, 0)

                    if now - last < interval:
                        continue

                    camera = camera_service.get_camera(camera_id)

                    if not camera:
                        continue
                    
                    frame = camera.read()

                    if frame is None:
                        continue

                    context = Frame(
                        camera_id=camera_id,
                        image=frame
                    )

                    try:
                        result = recognition_service.process_frame(context)
                        stream_manager = camera_service.stream_manager
                        stream_manager.set_recognition_state(camera_id, result)

                        logger.debug(
                            f"Recognition processed for {camera_id}"
                        )

                        for recognition in result.get("results", []):

                            match = recognition.get("match", {})
                            face = recognition.get("face", {})

                            if match.get("matched"):

                                event_bus.publish(
                                    "FACE_RECOGNIZED",
                                    {
                                        "camera_id": camera_id,
                                        "person_id": match.get("person_id"),
                                        "confidence": match.get("confidence")
                                    }
                                )

                                event_bus.publish(
                                    "ACCESS_GRANTED",
                                    {
                                        "camera_id": camera_id,
                                        "person_id": match.get("person_id"),
                                        "confidence": match.get("confidence")
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

                        self._last_run_by_camera[camera_id] = now

                    except Exception as error:
                        logger.error(
                            f"Recognition error for '{camera_id}': {error}"
                        )

            except Exception as error:
                logger.error(f"Recognition worker failure: {error}")

            time.sleep(0.05)  # loop leve (não depende mais do processamento)