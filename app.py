from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.detect import detect_bp
import os
import logging

# -----------------------------
# Logging Configuration
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------
# Flask App
# -----------------------------
app = Flask(__name__)

# -----------------------------
# Enable CORS
# -----------------------------
CORS(app)

# -----------------------------
# Upload Folder
# -----------------------------
UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -----------------------------
# Register Blueprint
# -----------------------------
app.register_blueprint(detect_bp)

logger.info("Facial Emotion Recognition API Started")

# -----------------------------
# Health Check
# -----------------------------
@app.route("/", methods=["GET"])
def home():
    return {
        "status": "running",
        "message": "Facial Emotion Recognition API is live",
        "model": "DeepFace"
    }, 200

# -----------------------------
# Backend Test
# -----------------------------
@app.route("/test", methods=["GET"])
def test():
    return {
        "status": "success",
        "message": "Backend working properly"
    }, 200

# -----------------------------
# Version Check
# -----------------------------
@app.route("/version", methods=["GET"])
def version():
    return {
        "commit": "32092e8",
        "message": "Latest backend deployed",
        "cors": "CORS(app)"
    }, 200

# -----------------------------
# Serve Uploaded Images
# -----------------------------
@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )

# -----------------------------
# Local Development
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )