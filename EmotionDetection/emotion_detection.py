"""Detect emotions using the Watson NLP laboratory endpoint."""
from typing import Any
import requests
URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}
EMOTION_NAMES = ("anger", "disgust", "fear", "joy", "sadness")
def empty_result() -> dict[str, Any]:
    """Return the result used for invalid or empty input."""
    return {name: None for name in (*EMOTION_NAMES, "dominant_emotion")}
def emotion_detector(text_to_analyze: str | None) -> dict[str, Any]:
    """Detect five emotions and return the dominant emotion."""
    if not text_to_analyze or not text_to_analyze.strip():
        return empty_result()
    payload = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(
        URL,
        headers=HEADERS,
        json=payload,
        timeout=10,
    )
    if response.status_code == 400:
        return empty_result()
    response.raise_for_status()
    emotions = response.json()["emotionPredictions"][0]["emotion"]
    dominant = max(EMOTION_NAMES, key=emotions.get)
    return {
        **{name: emotions[name] for name in EMOTION_NAMES},
        "dominant_emotion": dominant,
    }
