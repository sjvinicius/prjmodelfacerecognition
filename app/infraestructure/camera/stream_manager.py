from typing import Dict, Optional

from app.core.logger import logger
from app.infrastructure.camera.base_camera import BaseCamera
from app.infrastructure.camera.frame import Frame


class StreamManager:

    def __init__(self):
        self._cameras: Dict[str, BaseCamera] = {}

    def register_camera(
        self,
        camera_id: str,
        camera: BaseCamera
    ) -> None:

        if camera_id in self._cameras:
            logger.warning(
                f"Camera '{camera_id}' already registered"
            )
            return

        self._cameras[camera_id] = camera

        logger.info(
            f"Camera '{camera_id}' registered"
        )

    def start_camera(self, camera_id: str) -> None:
        camera = self._cameras.get(camera_id)

        if not camera:
            raise ValueError(
                f"Camera '{camera_id}' not found"
            )

        camera.start()

        logger.info(
            f"Camera '{camera_id}' started"
        )

    def stop_camera(self, camera_id: str) -> None:
        camera = self._cameras.get(camera_id)

        if not camera:
            return

        camera.stop()

        logger.info(
            f"Camera '{camera_id}' stopped"
        )

    def get_frame(
        self,
        camera_id: str
    ) -> Optional[Frame]:

        camera = self._cameras.get(camera_id)

        if not camera:
            return None

        image = camera.read()

        if image is None:
            return None

        return Frame(
            camera_id=camera_id,
            image=image
        )

    def remove_camera(self, camera_id: str) -> None:
        camera = self._cameras.get(camera_id)

        if not camera:
            return

        camera.stop()

        del self._cameras[camera_id]

        logger.info(
            f"Camera '{camera_id}' removed"
        )

    def list_cameras(self) -> list[str]:
        return list(self._cameras.keys())