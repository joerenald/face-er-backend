import cv2
import os

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def detect_face(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=6,
        minSize=(100, 100)
    )

    if len(faces) == 0:
        return None

    # Largest face
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])

    # Crop face
    face = image[y:y+h, x:x+w]

    cropped_path = os.path.join(
        "uploads",
        "cropped_face.jpg"
    )

    cv2.imwrite(cropped_path, face)

    # Draw rectangle on original image
    cv2.rectangle(
        image,
        (x, y),
        (x + w, y + h),
        (0, 255, 0),
        3
    )

    annotated_path = os.path.join(
        "uploads",
        "result.jpg"
    )

    cv2.imwrite(annotated_path, image)

    return {
    "face_path": cropped_path,
    "result_path": annotated_path,
    "x": int(x),
    "y": int(y),
    "w": int(w),
    "h": int(h)
}