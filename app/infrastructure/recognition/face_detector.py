from app.core.logger import logger
from app.infrastructure.camera.frame import Frame


class FaceDetector:

    def detect(
        self,
        frame: Frame
    ) -> list[dict]:

        logger.info(
            f"Detecting faces from camera '{frame.camera_id}'"
        )

        height, width = frame.image.shape[:2]

        mock_face = {
            "bbox": [
                int(width * 0.3),
                int(height * 0.2),
                int(width * 0.7),
                int(height * 0.8)
            ],
            "confidence": 0.99
        }

        return [mock_face]