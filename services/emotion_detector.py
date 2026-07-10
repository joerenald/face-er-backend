from deepface import DeepFace
from deepface.modules import modeling
import traceback

print("=" * 60)
print("Loading DeepFace Emotion Model...")
print("=" * 60)

# Load the emotion model once when the server starts
try:
    emotion_model = modeling.build_model("Emotion")
    print("✅ Emotion model loaded successfully.")
except Exception as e:
    print("❌ Error loading emotion model:", e)

print("=" * 60)


def detect_emotion(image_path):

    print("\n========== DEEPFACE ANALYSIS STARTED ==========")
    print("Image Path:", image_path)

    try:

        result = DeepFace.analyze(
            img_path=image_path,
            actions=["emotion"],
            detector_backend="opencv",
            enforce_detection=False,
            silent=True
        )

        if isinstance(result, list):
            result = result[0]

        emotion = result["dominant_emotion"].capitalize()
        confidence = float(
            result["emotion"][result["dominant_emotion"]]
        )

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