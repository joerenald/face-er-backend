from deepface import DeepFace
import traceback

print("====================================")
print("Loading DeepFace Emotion Model...")
print("====================================")

# Warm up the model once when the server starts
try:
    DeepFace.analyze(
        img_path="tests/warmup.jpg",   # Any small face image
        actions=["emotion"],
        enforce_detection=False,
        detector_backend="opencv",
        silent=True
    )
except:
    # Ignore if warmup image doesn't exist
    pass

print("DeepFace Model Loaded Successfully")


def detect_emotion(image_path):

    print("\n========== DEEPFACE ANALYSIS STARTED ==========")
    print("Image Path:", image_path)

    try:

        result = DeepFace.analyze(
            img_path=image_path,
            actions=["emotion"],
            enforce_detection=False,
            detector_backend="opencv",
            silent=True
        )

        if isinstance(result, list):
            result = result[0]

        emotion = result["dominant_emotion"].capitalize()
        confidence = float(result["emotion"][result["dominant_emotion"]])

        return {
            "success": True,
            "emotion": emotion,
            "confidence": round(confidence, 2)
        }

    except Exception as e:

        traceback.print_exc()

        return {
            "success": False,
            "message": str(e)
        }