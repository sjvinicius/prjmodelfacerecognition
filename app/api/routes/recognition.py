from flask import Blueprint, jsonify, request

from app.core.logger import logger
from app.services.recognition_service import (
    recognition_service
)

recognition_bp = Blueprint(
    "recognition",
    __name__,
    url_prefix="/recognition"
)


@recognition_bp.route("/process", methods=["POST"])
def process_recognition():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Invalid request body"
        }), 400

    camera_id = data.get("camera_id")

    if not camera_id:
        return jsonify({
            "error": "camera_id is required"
        }), 400

    try:

        result = recognition_service.process_camera(
            camera_id=camera_id
        )

        return jsonify(result), 200

    except Exception as error:

        logger.error(str(error))

        return jsonify({
            "error": str(error)
        }), 500