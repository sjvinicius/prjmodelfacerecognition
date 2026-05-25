import cv2
import numpy as np

from app.core.logger import logger

from app.infrastructure.recognition.insightface_detector import (
    InsightFaceDetector
)

from app.infrastructure.recognition.insightface_embedding_generator import (
    InsightFaceEmbeddingGenerator
)

from app.infrastructure.sync.supabase_client import (
    SupabaseClient
)

from app.services.recognition_service import (
    recognition_service
)


class EnrollmentQueueService:

    def __init__(self):

        self.supabase = (
            SupabaseClient()
        )

        self.detector = (
            InsightFaceDetector()
        )

        self.embedding_generator = (
            InsightFaceEmbeddingGenerator()
        )

    def download_private_image(
        self,
        path: str
    ):

        file_bytes = (
            self.supabase
            .client
            .storage
            .from_("faces")
            .download(path)
        )

        image_array = np.frombuffer(
            file_bytes,
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

    def list_pending(self) -> list[dict]:

        response = (
            self.supabase
            .client
            .table("filaembeddingfacerecog")
            .select("*")
            .eq("status", "P")
            .limit(10)
            .execute()
        )

        return response.data or []

    def mark_processing(
        self,
        queue_id: str
    ) -> None:

        (
            self.supabase
            .client
            .table("filaembeddingfacerecog")
            .update({
                "status": "N"
            })
            .eq(
                "filaembeddingfacerecog_id",
                queue_id
            )
            .execute()
        )

    def mark_completed(
        self,
        queue_id: str
    ) -> None:

        (
            self.supabase
            .client
            .table("filaembeddingfacerecog")
            .update({
                "status": "C"
            })
            .eq(
                "filaembeddingfacerecog_id",
                queue_id
            )
            .execute()
        )

    def mark_failed(
        self,
        queue_id: str,
        error: str
    ) -> None:

        (
            self.supabase
            .client
            .table("filaembeddingfacerecog")
            .update({
                "status": "X",
                "error": error
            })
            .eq(
                "filaembeddingfacerecog_id",
                queue_id
            )
            .execute()
        )

    def process_enrollment(
        self,
        user_id: str,
        storage_path: str
    ) -> None:

        logger.info(
            f"Processing enrollment for user '{user_id}'"
        )

        # baixa imagem
        image = self.download_private_image(
            storage_path
        )

        # detecta rostos
        faces = (
            self.detector
            .detect_image(image)
        )

        if not faces:

            raise Exception(
                "No face detected"
            )

        # pega maior face
        face = max(
            faces,
            key=lambda f:
            f["confidence"]
        )

        # gera embedding
        embedding = (
            self.embedding_generator
            .generate(face)
        )

        if isinstance(
            embedding,
            np.ndarray
        ):
            embedding = embedding.tolist()

        # salva no banco
        (
            self.supabase
            .client
            .table("facesautorizadas")
            .insert({
                "usuario_id": str(user_id),
                "storage_path": storage_path,
                "embedding": embedding
            })
            .execute()
        )

        # registra em memória
        recognition_service.register_face(
            person_id=str(user_id),
            embedding=np.array(
                embedding,
                dtype=np.float32
            )
        )

        logger.info(
            f"Enrollment completed "
            f"for user '{user_id}'"
        )


enrollment_queue_service = (
    EnrollmentQueueService()
)