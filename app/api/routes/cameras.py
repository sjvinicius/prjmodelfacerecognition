import cv2
import time

from flask import Blueprint, jsonify, request
from app.core.logger import logger
from app.services.camera_service import camera_service
from app.services.recognition_service import (
    recognition_service
)
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

        camera = camera_service.get_camera(camera_id)

        if not camera:
            return

        while True:

            frame = camera._latest_frame

            if frame is None:
                time.sleep(0.01)
                continue

            image = frame.copy()

            recognition_result = getattr(
                camera,
                "recognition_state",
                {"results": []}
            )

            for result in recognition_result.get("results", []):

                face = result.get("face", {})
                match = result.get("match", {})

                x1, y1, x2, y2 = face.get("bbox", (0, 0, 0, 0))

                cv2.rectangle(
                    image,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                label = "Unknown"

                if match.get("matched"):
                    label = f"{match.get('person_id')} ({match.get('confidence', 0):.2f})"

                cv2.putText(
                    image,
                    label,
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

            success, buffer = cv2.imencode(".jpg", image)

            if not success:
                continue

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" +
                buffer.tobytes() +
                b"\r\n"
            )

            time.sleep(0.03)

    return Response(
        generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        },
        direct_passthrough=True
    )

@cameras_bp.route("/<camera_id>/viewer", methods=["GET"])
def view_camera(camera_id: str):

    return f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Camera Stream</title>

            <style>
                body {{
                    margin: 0;
                    background: #111;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }}

                img {{
                    max-width: 100%;
                    max-height: 100%;
                    border: 2px solid #333;
                    border-radius: 8px;
                }}
            </style>
        </head>

        <body>
            <img src="/cameras/{camera_id}/stream">
        </body>
    </html>
    """