import random

from app.core.logger import logger


class EmbeddingGenerator:

    def generate(
        self,
        face: dict
    ) -> list[float]:

        logger.info(
            "Generating facial embedding"
        )

        embedding = [
            random.uniform(-1, 1)
            for _ in range(128)
        ]

        return embedding