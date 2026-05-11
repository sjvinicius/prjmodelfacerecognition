import threading
import time
from typing import Optional

import numpy as np

from app.core.logger import logger
from app.infrastructure.camera.base_camera import BaseCamera


class ThreadedCamera(BaseCamera):

    def __init__(
        self,
        camera: BaseCamera
    ):
        self.camera = camera

        self._thread: Optional[threading.Thread] = None

        self._is_running = False

        self._latest_frame: Optional[np.ndarray] = None

        self._lock = threading.Lock()

    def start(self) -> None:

        if self._is_running:
            logger.warning(
                "Threaded camera already running"
            )
            return

        self.camera.start()

        self._is_running = True

        self._thread = threading.Thread(
            target=self._update,
            daemon=True
        )

        self._thread.start()

        logger.info(
            "Threaded camera started"
        )

    def _update(self) -> None:

        while self._is_running:

            frame = self.camera.read()

            if frame is None:
                time.sleep(0.01)
                continue

            with self._lock:
                self._latest_frame = frame

    def read(self) -> Optional[np.ndarray]:

        with self._lock:

            if self._latest_frame is None:
                return None

            return self._latest_frame.copy()

    def stop(self) -> None:

        self._is_running = False

        self.camera.stop()

        logger.info(
            "Threaded camera stopped"
        )

    def is_opened(self) -> bool:
        return self.camera.is_opened()