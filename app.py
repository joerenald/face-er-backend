from flask import Flask
from flask_cors import CORS
from routes.detect import detect_bp
from flask import send_from_directory
import os
app = Flask(__name__)

CORS(app)

app.register_blueprint(detect_bp)

@app.route("/")
def home():
    return "Facial Emotion Recognition Backend Running"
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        os.path.join(app.root_path, "uploads"),
        filename
    )
if __name__ == "__main__":
    app.run(debug=True)