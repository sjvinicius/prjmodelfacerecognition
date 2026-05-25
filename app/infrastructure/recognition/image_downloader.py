import cv2
import numpy as np
import requests

from app.core.logger import logger


class ImageDownloader:

    @staticmethod
    def download_image(
        url: str
    ):

        try:

            response = requests.get(
                url,
                timeout=15
            )

            response.raise_for_status()

            image_array = np.frombuffer(
                response.content,
                dtype=np.uint8
            )

            image = cv2.imdecode(
                image_array,
                cv2.IMREAD_COLOR
            )

            if image is None:

                raise Exception(
                    "Failed to decode image"
                )

            return image

        except Exception as error:

            logger.error(
                f"Failed to download image: "
                f"{error}"
            )

            raise