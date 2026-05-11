import random

from app.core.logger import logger


class Recognizer:

    def recognize(
        self,
        embedding: list[float]
    ) -> dict:

        logger.info(
            "Recognizing facial embedding"
        )

        recognized = random.choice([True, False])

        if recognized:

            return {
                "matched": True,
                "person_id": "user_123",
                "confidence": round(
                    random.uniform(0.80, 0.99),
                    2
                )
            }

        return {
            "matched": False,
            "person_id": None,
            "confidence": round(
                random.uniform(0.10, 0.40),
                2
            )
        }