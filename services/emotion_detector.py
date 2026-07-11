from deepface import DeepFace
import traceback
import logging

# ---------------------------------------
# Logging Configuration
# ---------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("=" * 60)
logger.info("DeepFace Emotion Detector Initialized")
logger.info("=" * 60)


def detect_emotion(image_path):
    """
    Detect the dominant emotion from the cropped face image.
    """

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

        dominant = result["dominant_emotion"]

        return {
            "success": True,
            "emotion": dominant.capitalize(),
            "confidence": round(
                float(result["emotion"][dominant]),
                2
            )
        }

    except Exception as e:

        logger.exception("Emotion detection failed")

        return {
            "success": False,
            "message": str(e)
        }