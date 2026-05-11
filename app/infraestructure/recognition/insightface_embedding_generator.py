import numpy as np

from app.core.logger import logger


class InsightFaceEmbeddingGenerator:

    def generate(
        self,
        face: dict
    ) -> np.ndarray:

        logger.info(
            "Generating InsightFace embedding"
        )

        face_object = face.get("face_object")

        if face_object is None:
            raise ValueError(
                "Face object not found"
            )

        embedding = face_object.embedding

        return embedding