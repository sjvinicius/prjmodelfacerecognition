import numpy as np

from app.core.logger import logger

from app.infrastructure.recognition.cosine_recognizer import (
    CosineRecognizer
)

from app.infrastructure.recognition.face_registry import (
    FaceRegistry
)

from app.infrastructure.recognition.insightface_detector import (
    InsightFaceDetector
)

from app.infrastructure.recognition.insightface_embedding_generator import (
    InsightFaceEmbeddingGenerator
)

from app.infrastructure.recognition.recognition_pipeline import (
    RecognitionPipeline
)

from app.services.camera_service import camera_service


class RecognitionService:

    def __init__(self):

        self.registry = FaceRegistry()

        detector = InsightFaceDetector()

        embedding_generator = (
            InsightFaceEmbeddingGenerator()
        )

        recognizer = CosineRecognizer(
            registry=self.registry
        )

        self.pipeline = RecognitionPipeline(
            detector=detector,
            embedding_generator=embedding_generator,
            recognizer=recognizer
        )

    def process_camera(
        self,
        camera_id: str
    ) -> dict:

        logger.info(
            f"Processing recognition for camera '{camera_id}'"
        )

        frame = camera_service.get_frame(camera_id)

        if frame is None:
            raise ValueError(
                f"No frame available for camera '{camera_id}'"
            )

        result = self.pipeline.process(frame)

        return result

    def register_face(
        self,
        person_id: str,
        embedding: np.ndarray
    ) -> None:

        self.registry.register(
            person_id=person_id,
            embedding=embedding
        )

    def remove_face(
        self,
        person_id: str
    ) -> None:

        self.registry.remove(person_id)

    def total_faces(self) -> int:
        return self.registry.count()

    def process_frame(
        self,
        frame
    ) -> dict:

        logger.info(
            f"RECSERVICE | Processing frame from camera '{frame.camera_id}'"
        )

        return self.pipeline.process(frame)


recognition_service = RecognitionService()