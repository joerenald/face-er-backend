from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from services.face_detector import detect_face
from services.emotion_detector import detect_emotion
import os
import traceback

detect_bp = Blueprint("detect", __name__)

UPLOAD_FOLDER = "uploads"

def get_emotion_color(emotion):

    colors = {
        "Happy": (0, 255, 0),         # Green
        "Neutral": (255, 180, 0),     # Orange
        "Sad": (255, 180, 0),         # Cyan
        "Angry": (0, 0, 255),         # Red
        "Fear": (255, 0, 255),        # Purple
        "Surprise": (0, 165, 255),    # Orange
        "Disgust": (0, 128, 0)        # Dark Green
    }

    return colors.get(emotion, (0, 255, 0))
@detect_bp.route("/detect", methods=["POST"])
def detect():

    print("\n========== DETECT API CALLED ==========")

    try:

        # -----------------------------
        # Check image uploaded
        # -----------------------------
        if "image" not in request.files:
            print("No image received.")

            return jsonify({
                "success": False,
                "message": "No image uploaded."
            }), 400

        image = request.files["image"]

        if image.filename == "":
            print("Empty filename.")

            return jsonify({
                "success": False,
                "message": "No file selected."
            }), 400

        # -----------------------------
        # Save uploaded image
        # -----------------------------
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        filename = secure_filename(image.filename)

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        image.save(filepath)

        print("Image saved successfully.")
        print("Path :", filepath)

        # -----------------------------
        # Detect Face
        # -----------------------------
        face_data = detect_face(filepath)

        if face_data is None:

            print("No human face detected.")

            return jsonify({
                "success": False,
                "message": "No human face detected."
            })

        cropped_face = face_data["face_path"]
        result_image = face_data["result_path"]

        print("Face detected.")
        print("Cropped Face :", cropped_face)

        # -----------------------------
        # Detect Emotion
        # -----------------------------
        result = detect_emotion(cropped_face)
        
        if result["success"]:

         import cv2

         image = cv2.imread(result_image)

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

         result["image"] = "http://127.0.0.1:5000/uploads/result.jpg"

        print("Result :", result)

        return jsonify(result)

    except Exception as e:

        print("\n========== BACKEND ERROR ==========")

        traceback.print_exc()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500