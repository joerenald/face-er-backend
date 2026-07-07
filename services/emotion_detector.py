from deepface import DeepFace
import traceback


def detect_emotion(image_path):

    print("\n========== DEEPFACE ANALYSIS STARTED ==========")
    print("Image Path:", image_path)

    try:

        result = DeepFace.analyze(
            img_path=image_path,
            actions=["emotion"],
            enforce_detection=False,
            detector_backend="opencv"
        )

        print("DeepFace analysis completed.")

        # DeepFace may return a list
        if isinstance(result, list):
            result = result[0]

        # Extract emotion
        emotion = str(result["dominant_emotion"])

        # Convert NumPy float32 to Python float
        confidence = float(result["emotion"][emotion])

        response = {
            "success": True,
            "emotion": emotion.capitalize(),
            "confidence": round(confidence, 2)
        }

        print("Response:", response)

        return response

    except Exception as e:

        print("\n========== DEEPFACE ERROR ==========")
        traceback.print_exc()

        return {
            "success": False,
            "message": str(e)
        }