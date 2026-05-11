from insightface.app import FaceAnalysis

from app.core.logger import logger
from app.infrastructure.camera.frame import Frame

class InsightFaceDetector:

    def __init__(self):

        logger.info(
            "Initializing InsightFace detector"
        )

        self.app = FaceAnalysis(
            name="buffalo_l"
        )

        self.app.prepare(
            ctx_id=0,
            det_size=(640, 640)
        )

    def detect(
        self,
        frame: Frame
    ) -> list[dict]:

        logger.info(
            f"Running InsightFace detection for camera '{frame.camera_id}'"
        )

        faces = self.app.get(frame.image)

        results = []

        for face in faces:

            bbox = face.bbox.astype(int).tolist()

            results.append({
                "bbox": bbox,
                "confidence": float(face.det_score),
                "face_object": face
            })

        return results