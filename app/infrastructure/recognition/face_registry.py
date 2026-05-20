from typing import Optional

import numpy as np

from app.core.logger import logger


class FaceRegistry:

    def __init__(self):

        self._faces: dict[str, np.ndarray] = {}

    def register(
        self,
        person_id: str,
        embedding: np.ndarray
    ) -> None:

        logger.info(
            f"Registering face '{person_id}'"
        )

        self._faces[person_id] = embedding

    def remove(
        self,
        person_id: str
    ) -> None:

        if person_id not in self._faces:
            return

        del self._faces[person_id]

        logger.info(
            f"Removed face '{person_id}'"
        )

    def get(
        self,
        person_id: str
    ) -> Optional[np.ndarray]:

        return self._faces.get(person_id)

    def get_all(self) -> list[dict]:

        return [
            {
                "person_id": person_id,
                "embedding": embedding
            }
            for person_id, embedding
            in self._faces.items()
        ]

    def clear(self) -> None:

        self._faces.clear()

        logger.info(
            "Face registry cleared"
        )

    def count(self) -> int:
        return len(self._faces)