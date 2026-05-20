from typing import Optional

import cv2
import numpy as np

from app.core.logger import logger
from app.infrastructure.camera.base_camera import BaseCamera
from app.core.config import settings


class USBCamera(BaseCamera):

    def __init__(self, device_index: int = 0):
        self.device_index = device_index
        self.capture = None

    def start(self) -> None:
        self.capture = cv2.VideoCapture(self.device_index)

        if not self.capture.isOpened():
            raise RuntimeError("Failed to open camera")

        logger.info(f"USB camera {self.device_index} started")

    def read(self) -> Optional[np.ndarray]:
        if not self.capture:
            return None

        success, frame = self.capture.read()

        if not success:
            return None

        return frame

    def stop(self) -> None:
        if self.capture:
            self.capture.release()

        self.capture = None

    def is_opened(self) -> bool:
        return self.capture is not None and self.capture.isOpened()