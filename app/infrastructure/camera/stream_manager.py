from typing import Dict, Optional
import numpy as np

from app.core.logger import logger
from app.infrastructure.camera.base_camera import BaseCamera


class StreamManager:

    def __init__(self):
        self._cameras: Dict[str, BaseCamera] = {}
        self._recognition_state: Dict[str, dict] = {}

    def register_camera(self, camera_id: str, camera: BaseCamera) -> None:

        if camera_id in self._cameras:
            logger.warning(f"Camera '{camera_id}' already registered")
            return

        self._cameras[camera_id] = camera

        logger.info(f"Camera '{camera_id}' registered")

    def start_camera(self, camera_id: str) -> None:

        camera = self._cameras.get(camera_id)

        if not camera:
            raise ValueError(f"Camera '{camera_id}' not found")

        camera.start()

        logger.info(f"Camera '{camera_id}' started")

    def stop_camera(self, camera_id: str) -> None:

        camera = self._cameras.get(camera_id)

        if not camera:
            return

        camera.stop()

        logger.info(f"Camera '{camera_id}' stopped")

    def get_frame(self, camera_id: str) -> Optional[np.ndarray]:

        camera = self._cameras.get(camera_id)

        if not camera:
            return None

        frame = camera.read()

        if frame is None:
            return None

        return frame

    def remove_camera(self, camera_id: str) -> None:

        camera = self._cameras.get(camera_id)

        if not camera:
            return

        camera.stop()

        del self._cameras[camera_id]

        logger.info(f"Camera '{camera_id}' removed")

    def list_cameras(self) -> list[str]:
        return list(self._cameras.keys())

    def get_camera(self, camera_id: str) -> Optional[BaseCamera]:
        return self._cameras.get(camera_id)

    def set_recognition_state(self, camera_id: str, state: dict):
        self._recognition_state[camera_id] = state
        
    def get_recognition_state(self, camera_id: str):
        return self._recognition_state.get(camera_id, {"results": []})