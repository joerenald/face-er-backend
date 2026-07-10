import cv2
import os

UPLOAD_FOLDER = "uploads"

# Load Haar Cascade once
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


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

    # Largest detected face
    x, y, w, h = max(
        faces,
        key=lambda face: face[2] * face[3]
    )

    # Add padding
    padding = 20

    x1 = max(0, x - padding)
    y1 = max(0, y - padding)
    x2 = min(image.shape[1], x + w + padding)
    y2 = min(image.shape[0], y + h + padding)

    # Crop face
    face = image[y1:y2, x1:x2]

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    cropped_path = os.path.join(
        UPLOAD_FOLDER,
        "cropped_face.jpg"
    )

    # Save cropped face
    cv2.imwrite(
        cropped_path,
        face
    )

    # Draw bounding box
    cv2.rectangle(
        image,
        (x1, y1),
        (x2, y2),
        (0, 255, 0),
        3
    )

    annotated_path = os.path.join(
        UPLOAD_FOLDER,
        "result.jpg"
    )

    # Save annotated image
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