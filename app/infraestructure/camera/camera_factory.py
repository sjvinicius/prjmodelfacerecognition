from app.infrastructure.camera.base_camera import BaseCamera
from app.infrastructure.camera.threaded_camera import ThreadedCamera
from app.infrastructure.camera.usb_camera import USBCamera


class CameraFactory:

    @staticmethod
    def create(
        camera_type: str,
        **kwargs
    ) -> BaseCamera:

        camera_type = camera_type.lower()

        if camera_type == "usb":

            camera = USBCamera(
                device_index=kwargs.get("device_index", 0)
            )

            return ThreadedCamera(camera)

        raise ValueError(
            f"Unsupported camera type '{camera_type}'"
        )