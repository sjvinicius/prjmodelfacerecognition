from flask import Flask

from app.core.config import settings
from app.core.logger import logger

from app.api.routes.cameras import cameras_bp
from app.api.routes.recognition import recognition_bp
from app.services.camera_service import camera_service
from app.workers.recognition_worker import RecognitionWorker
from app.workers.event_queue_worker import EventQueueWorker
from app.workers.storage_cleanup_worker import StorageCleanupWorker
from app.workers.sync_worker import SyncWorker


def create_app() -> Flask:
    app = Flask(__name__)

    camera_service.create_camera(
        camera_id="default",
        camera_type="usb",
        device_index=0
    )

    camera_service.start_camera("default")

    recognition_worker = RecognitionWorker()
    recognition_worker.start()

    event_queue_worker = EventQueueWorker()
    event_queue_worker.start()

    storage_cleanup_worker = StorageCleanupWorker()
    storage_cleanup_worker.start()

    sync_worker = SyncWorker()
    sync_worker.start()

    app.config["APP_NAME"] = settings.APP_NAME
    app.config["DEBUG"] = settings.DEBUG

    register_routes(app)

    app.register_blueprint(cameras_bp)
    app.register_blueprint(recognition_bp)

    logger.info(f"{settings.APP_NAME} initialized")

    return app


def register_routes(app: Flask) -> None:
    from app.api.routes.health import health_bp

    app.register_blueprint(health_bp)