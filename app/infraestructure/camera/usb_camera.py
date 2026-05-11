from typing import Optional

import cv2
import numpy as np

from app.core.logger import logger
from app.infrastructure.camera.base_camera import BaseCamera
from app.core.config import settings


class USBCamera(BaseCamera):

    def __init__(
        self,
        device_index: int = 0
    ):
        self.device_index = device_index

        self.capture: Optional[cv2.VideoCapture] = None

        self._is_running = False

    def start(self) -> None:

        if self._is_running:
            logger.warning(
                f"USB camera '{self.device_index}' already running"
            )
            return

        self.capture = cv2.VideoCapture(self.device_index)

        if not self.capture.isOpened():
            raise RuntimeError(
                f"Failed to open USB camera '{self.device_index}'"
            )

        self.capture.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            settings.CAMERA_FRAME_WIDTH
        )

        self.capture.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            settings.CAMERA_FRAME_HEIGHT
        )

        self.capture.set(
            cv2.CAP_PROP_FPS,
            settings.CAMERA_FPS
        )

        self._is_running = True

        logger.info(
            f"USB camera '{self.device_index}' started"
        )

    def read(self) -> Optional[np.ndarray]:

        if not self.capture or not self._is_running:
            return None

        success, frame = self.capture.read()

        if not success:
            logger.warning(
                f"Failed to read frame from USB camera '{self.device_index}'"
            )
            return None

        return frame

    def stop(self) -> None:

        if self.capture:
            self.capture.release()

        self._is_running = False

        logger.info(
            f"USB camera '{self.device_index}' stopped"
        )

    def is_opened(self) -> bool:
        return self._is_running