from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.detect import detect_bp
import os

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Enable CORS
CORS(app)

# Register API
app.register_blueprint(detect_bp)

# Health Check
@app.route("/")
def home():
    return {
        "status": "running",
        "message": "Facial Emotion Recognition API is live",
        "model": "DeepFace"
    }

# Test Route
@app.route("/test")
def test():
    return {
        "status": "success",
        "message": "Backend working properly"
    }

# Serve Result Images
@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 7860))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )