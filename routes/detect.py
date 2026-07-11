from flask import Blueprint, request, jsonify
from services.face_detector import detect_face
from services.emotion_detector import detect_emotion

from cloudinary.uploader import upload
from config.cloudinary_config import *

import os
import uuid
import cv2
import base64
import traceback

detect_bp = Blueprint("detect", __name__)

# -------------------------------------------------------
# Upload Folder
# -------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -------------------------------------------------------
# Emotion Label Colors
# -------------------------------------------------------
def get_emotion_color(emotion):
    colors = {
        "Happy": (0, 255, 0),
        "Neutral": (255, 180, 0),
        "Sad": (255, 180, 0),
        "Angry": (0, 0, 255),
        "Fear": (255, 0, 255),
        "Surprise": (0, 165, 255),
        "Disgust": (0, 128, 0)
    }

    return colors.get(emotion, (0, 255, 0))


# -------------------------------------------------------
# Detect Emotion API
# -------------------------------------------------------
@detect_bp.route("/detect", methods=["POST"])
def detect():

    filepath = None
    cropped_face = None
    result_image = None

    try:

        # ---------------------------------------------------
        # Validate Request
        # ---------------------------------------------------
        if "image" not in request.files:
            return jsonify({
                "success": False,
                "message": "No image uploaded."
            }), 400

        image = request.files["image"]

        if image.filename == "":
            return jsonify({
                "success": False,
                "message": "No file selected."
            }), 400

        # ---------------------------------------------------
        # Save Uploaded Image
        # ---------------------------------------------------
        filename = f"{uuid.uuid4().hex}.jpg"

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        image.save(filepath)

        # ---------------------------------------------------
        # Upload Original Image to Cloudinary
        # ---------------------------------------------------
        original_upload = upload(
            filepath,
            folder="Face-ER/original"
        )

        original_url = original_upload["secure_url"]

        # ---------------------------------------------------
        # Face Detection
        # ---------------------------------------------------
        face_data = detect_face(filepath)

        if face_data is None:
            return jsonify({
                "success": False,
                "message": "No human face detected."
            }), 400

        cropped_face = face_data["face_path"]
        result_image = face_data["result_path"]

        # ---------------------------------------------------
        # Emotion Detection
        # ---------------------------------------------------
        result = detect_emotion(cropped_face)

        if not result["success"]:
            return jsonify(result), 500

        # ---------------------------------------------------
        # Read Result Image
        # ---------------------------------------------------
        image = cv2.imread(result_image)

        if image is None:
            return jsonify({
                "success": False,
                "message": "Unable to process image."
            }), 500

        x = face_data["x"]
        y = face_data["y"]
        w = face_data["w"]
        h = face_data["h"]

        label = f'{result["emotion"]} ({result["confidence"]:.1f}%)'

        label_color = get_emotion_color(result["emotion"])

        (text_width, text_height), _ = cv2.getTextSize(
            label,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            2
        )

        padding = 12

        cv2.rectangle(
            image,
            (x, y - text_height - 20),
            (x + text_width + padding * 2, y),
            label_color,
            -1
        )

        cv2.putText(
            image,
            label,
            (x + padding, y - 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.imwrite(result_image, image)

        # ---------------------------------------------------
        # Upload Annotated Image to Cloudinary
        # ---------------------------------------------------
        result_upload = upload(
            result_image,
            folder="Face-ER/results"
        )

        result_url = result_upload["secure_url"]

        # ---------------------------------------------------
        # Convert Image to Base64
        # ---------------------------------------------------
        success, buffer = cv2.imencode(".jpg", image)

        if not success:
            return jsonify({
                "success": False,
                "message": "Failed to encode image."
            }), 500

        result["image"] = (
            "data:image/jpeg;base64,"
            + base64.b64encode(buffer).decode("utf-8")
        )

        # ---------------------------------------------------
        # Cloudinary URLs
        # ---------------------------------------------------
        result["original_url"] = original_url
        result["result_url"] = result_url

        return jsonify(result)

    except Exception as e:

        traceback.print_exc()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:

        # ---------------------------------------------------
        # Delete Temporary Local Files
        # ---------------------------------------------------
        for file in [filepath, cropped_face, result_image]:
            try:
                if file and os.path.exists(file):
                    os.remove(file)
            except Exception:
                pass