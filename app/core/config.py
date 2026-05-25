from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass(frozen=True)
class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Vision Edge")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 5000))

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))

    CAMERA_FRAME_WIDTH: int = int(os.getenv("CAMERA_FRAME_WIDTH", 640))
    CAMERA_FRAME_HEIGHT: int = int(os.getenv("CAMERA_FRAME_HEIGHT", 480))
    CAMERA_FPS: int = int(os.getenv("CAMERA_FPS", 20))

    RECOGNITION_THRESHOLD: float = float(
        os.getenv("RECOGNITION_THRESHOLD", 0.6)
    )

    FACE_DETECTION_CONFIDENCE: float = float(
        os.getenv("FACE_DETECTION_CONFIDENCE", 0.7)
    )
    
    FACE_SYNC_INTERVAL = int(
        os.getenv("FACE_SYNC_INTERVAL", 30)
    )
    
    RECOGNITION_INTERVAL = float(
        os.getenv("RECOGNITION_INTERVAL", 0.5)
    )
    
    EVENT_QUEUE_INTERVAL = float(
        os.getenv("EVENT_QUEUE_INTERVAL", 2)
    )

    ENROLLMENT_INTERVAL = float(
        os.getenv("ENROLLMENT_INTERVAL", 2)
    )
    
    STORAGE_CLEANUP_INTERVAL = int(
        os.getenv("STORAGE_CLEANUP_INTERVAL", 3600)
    )

    COMPLETED_RETENTION_DAYS = int(
        os.getenv("COMPLETED_RETENTION_DAYS", 1)
    )

    FAILED_RETENTION_DAYS = int(
        os.getenv("FAILED_RETENTION_DAYS", 7)
    )

    SNAPSHOT_RETENTION_DAYS = int(
        os.getenv("SNAPSHOT_RETENTION_DAYS", 3)
    )


settings = Settings()