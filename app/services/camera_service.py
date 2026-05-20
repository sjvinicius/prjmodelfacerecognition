from typing import Optional

from app.core.logger import logger
from app.infrastructure.camera.camera_factory import CameraFactory
from app.infrastructure.camera.frame import Frame
from app.infrastructure.camera.stream_manager import StreamManager

class CameraService:

    def __init__(self):
        self.stream_manager = StreamManager()

    def create_camera(
        self,
        camera_id: str,
        camera_type: str,
        **kwargs
    ) -> None:

        camera = CameraFactory.create(
            camera_type=camera_type,
            **kwargs
        )

        self.stream_manager.register_camera(
            camera_id=camera_id,
            camera=camera
        )

        logger.info(
            f"Camera '{camera_id}' created"
        )

    def start_camera(
        self,
        camera_id: str
    ) -> None:

        self.stream_manager.start_camera(camera_id)

    def stop_camera(
        self,
        camera_id: str
    ) -> None:

        self.stream_manager.stop_camera(camera_id)

    def remove_camera(
        self,
        camera_id: str
    ) -> None:

        self.stream_manager.remove_camera(camera_id)

    def get_frame(
        self,
        camera_id: str
    ) -> Optional[Frame]:
    
        return self.stream_manager.get_frame(camera_id)

    def list_cameras(self) -> list[str]:
        return self.stream_manager.list_cameras()

    def get_camera(self, camera_id: str):
        return self.stream_manager.get_camera(camera_id)

camera_service = CameraService()