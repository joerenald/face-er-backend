from flask import Flask, send_from_directory, request
from flask_cors import CORS
from routes.detect import detect_bp
import os
import logging

# -------------------------------------------------
# Logging Configuration
# -------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------------------------
# Flask App
# -------------------------------------------------
app = Flask(__name__)

# -------------------------------------------------
# Enable CORS
# -------------------------------------------------
CORS(app)

# -------------------------------------------------
# Upload Folder
# -------------------------------------------------
UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------------------------------------
# Log Every Request
# -------------------------------------------------
@app.before_request
def before_request():
    logger.info("=" * 60)
    logger.info(f"{request.method} {request.path}")
    logger.info(f"Origin: {request.headers.get('Origin')}")
    logger.info("=" * 60)

# -------------------------------------------------
# Log Response Headers
# -------------------------------------------------
@app.after_request
def after_request(response):
    logger.info(
        f"Access-Control-Allow-Origin: "
        f"{response.headers.get('Access-Control-Allow-Origin')}"
    )
    return response

# -------------------------------------------------
# Register Blueprints
# -------------------------------------------------
app.register_blueprint(detect_bp)

logger.info("Facial Emotion Recognition API Started")

# -------------------------------------------------
# Home Route
# -------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return {
        "status": "running",
        "message": "Facial Emotion Recognition API is live",
        "model": "DeepFace",
        "commit": "32092e8",
        "cors": "CORS(app)"
    }, 200

# -------------------------------------------------
# Test Route
# -------------------------------------------------
@app.route("/test", methods=["GET"])
def test():
    return {
        "status": "success",
        "message": "Backend working properly"
    }, 200

# -------------------------------------------------
# Debug Route
# -------------------------------------------------
@app.route("/debug", methods=["GET"])
def debug():
    return {
        "commit": "32092e8",
        "cors": "CORS(app)",
        "message": "Latest backend deployed"
    }, 200

# -------------------------------------------------
# Serve Uploaded Images
# -------------------------------------------------
@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )

# -------------------------------------------------
# Run App (Local Only)
# -------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )