import cv2
import os
import uuid

# -----------------------------
# Upload Folder
# -----------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -----------------------------
# Load Haar Cascade Once
# -----------------------------
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

if face_cascade.empty():
    raise RuntimeError("Failed to load Haar Cascade Classifier.")


def detect_face(image_path):
    """
    Detect the largest face in the image,
    crop it, and create an annotated image.
    """

    image = cv2.imread(image_path)

    if image is None:
        return None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.15,
        minNeighbors=5,
        minSize=(80, 80)
    )

    if len(faces) == 0:
        return None

    # -----------------------------
    # Select Largest Face
    # -----------------------------
    x, y, w, h = max(
        faces,
        key=lambda face: face[2] * face[3]
    )

    # -----------------------------
    # Add Padding
    # -----------------------------
    padding = 20

    x1 = max(0, x - padding)
    y1 = max(0, y - padding)
    x2 = min(image.shape[1], x + w + padding)
    y2 = min(image.shape[0], y + h + padding)

    # -----------------------------
    # Crop Face
    # -----------------------------
    face = image[y1:y2, x1:x2]

    # -----------------------------
    # Generate Unique File Names
    # -----------------------------
    unique_id = uuid.uuid4().hex

    cropped_path = os.path.join(
        UPLOAD_FOLDER,
        f"{unique_id}_cropped.jpg"
    )

    annotated_path = os.path.join(
        UPLOAD_FOLDER,
        f"{unique_id}_result.jpg"
    )

    # -----------------------------
    # Save Cropped Face
    # -----------------------------
    cv2.imwrite(
        cropped_path,
        face
    )

    # -----------------------------
    # Draw Bounding Box
    # -----------------------------
    cv2.rectangle(
        image,
        (x1, y1),
        (x2, y2),
        (0, 255, 0),
        3
    )

    # -----------------------------
    # Save Annotated Image
    # -----------------------------
    cv2.imwrite(
        annotated_path,
        image
    )

    return {
        "face_path": cropped_path,
        "result_path": annotated_path,
        "x": int(x1),
        "y": int(y1),
        "w": int(x2 - x1),
        "h": int(y2 - y1)
    }