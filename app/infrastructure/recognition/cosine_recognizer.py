import numpy as np

from app.core.config import settings
from app.core.logger import logger
from app.infrastructure.recognition.face_registry import (
    FaceRegistry
)


class CosineRecognizer:

    def __init__(
        self,
        registry: FaceRegistry
    ):
        self.registry = registry

    def recognize(
        self,
        embedding: np.ndarray
    ) -> dict:

        logger.info(
            "Running cosine similarity recognition"
        )

        known_faces = self.registry.get_all()

        best_match = None

        best_score = -1.0

        for known_face in known_faces:

            similarity = self._cosine_similarity(
                embedding,
                known_face["embedding"]
            )

            if similarity > best_score:

                best_score = similarity

                best_match = known_face

        if (
            best_match
            and best_score >= settings.RECOGNITION_THRESHOLD
        ):

            return {
                "matched": True,
                "person_id": best_match["person_id"],
                "confidence": round(float(best_score), 4)
            }

        return {
            "matched": False,
            "person_id": None,
            "confidence": round(float(best_score), 4)
        }

    def _cosine_similarity(
        self,
        embedding1: np.ndarray,
        embedding2: np.ndarray
    ) -> float:

        dot_product = np.dot(
            embedding1,
            embedding2
        )

        norm_a = np.linalg.norm(embedding1)

        norm_b = np.linalg.norm(embedding2)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        similarity = dot_product / (norm_a * norm_b)

        return float(similarity)