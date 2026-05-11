import cv2
import time

from flask import Blueprint, jsonify, request
from app.core.logger import logger
from app.services.camera_service import camera_service
from flask import Response

cameras_bp = Blueprint(
    "cameras",
    __name__,
    url_prefix="/cameras"
)

@cameras_bp.route("/<camera_id>/frame", methods=["GET"])
def get_camera_frame(camera_id: str):

    frame = camera_service.get_frame(camera_id)

    if frame is None:
        return jsonify({
            "error": "Frame not available"
        }), 404

    success, buffer = cv2.imencode(
        ".jpg",
        frame.image
    )

    if not success:
        return jsonify({
            "error": "Failed to encode frame"
        }), 500

    return Response(
        buffer.tobytes(),
        mimetype="image/jpeg"
    )

@cameras_bp.route("/start", methods=["POST"])
def start_camera():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Invalid request body"
        }), 400

    camera_id = data.get("camera_id")
    camera_type = data.get("camera_type", "usb")

    if not camera_id:
        return jsonify({
            "error": "camera_id is required"
        }), 400

    try:

        camera_service.create_camera(
            camera_id=camera_id,
            camera_type=camera_type,
            device_index=data.get("device_index", 0)
        )

        camera_service.start_camera(camera_id)

        logger.info(
            f"Camera '{camera_id}' started via API"
        )

        return jsonify({
            "status": "started",
            "camera_id": camera_id
        }), 200

    except Exception as error:

        logger.error(str(error))

        return jsonify({
            "error": str(error)
        }), 500


@cameras_bp.route("/", methods=["GET"])
def list_cameras():

    cameras = camera_service.list_cameras()

    return jsonify({
        "cameras": cameras
    }), 200
    
@cameras_bp.route("/<camera_id>/stream", methods=["GET"])
def stream_camera(camera_id: str):

    def generate():

        while True:

            frame = camera_service.get_frame(camera_id)

            if frame is None:
                time.sleep(0.01)
                continue

            success, buffer = cv2.imencode(
                ".jpg",
                frame.image
            )

            if not success:
                continue

            frame_bytes = buffer.tobytes()

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" +
                frame_bytes +
                b"\r\n"
            )

    return Response(
        generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )