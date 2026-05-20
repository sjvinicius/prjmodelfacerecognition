from app.core.logger import logger
from app.infrastructure.camera.frame import Frame

class RecognitionPipeline:

    def __init__(
        self,
        detector,
        embedding_generator,
        recognizer
    ):
        self.detector = detector

        self.embedding_generator = embedding_generator

        self.recognizer = recognizer

    def process(
        self,
        frame: Frame
    ) -> dict:

        logger.info(
            f"Processing frame from camera '{frame.camera_id}'"
        )

        faces = self.detector.detect(frame)

        results = []

        for face in faces:

            embedding = self.embedding_generator.generate(
                face
            )

            match = self.recognizer.recognize(
                embedding
            )

            results.append({
                "face": face,
                "match": match
            })

        return {
            "camera_id": frame.camera_id,
            "faces_detected": len(faces),
            "results": results
        }