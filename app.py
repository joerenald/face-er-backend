from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.detect import detect_bp
import os

app = Flask(__name__)

# Create uploads folder automatically
UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allow requests from your frontend
CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:5173",
                "https://face-er-frontend.vercel.app"
            ]
        }
    }
)

# Register routes
app.register_blueprint(detect_bp)

# Health Check
@app.route("/")
def home():
    return {
        "status": "running",
        "service": "Facial Emotion Recognition API",
        "model": "DeepFace"
    }

# Serve processed images
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7860,
        debug=False
    )