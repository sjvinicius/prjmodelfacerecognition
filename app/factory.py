from flask import Flask

from app.core.config import settings
from app.core.logger import logger

from app.api.routes.cameras import cameras_bp
from app.api.routes.recognition import recognition_bp

app.register_blueprint(cameras_bp)
app.register_blueprint(recognition_bp)

def create_app() -> Flask:
    app = Flask(__name__)

    app.config["APP_NAME"] = settings.APP_NAME
    app.config["DEBUG"] = settings.DEBUG

    register_routes(app)

    logger.info(f"{settings.APP_NAME} initialized")

    return app


def register_routes(app: Flask) -> None:
    from app.api.routes.health import health_bp

    app.register_blueprint(health_bp)