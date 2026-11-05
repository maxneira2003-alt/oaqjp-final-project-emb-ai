"""Flask web application for emotion detection."""

from flask import Flask, render_template, request

from EmotionDetection.emotion_detection import emotion_detector


app = Flask(__name__)


@app.route("/")
def index():
    """Render the application interface."""
    return render_template("index.html")


@app.route("/emotionDetector")
def emotion_detector_route():
    """Return emotion scores for the supplied text."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    result = emotion_detector(text_to_analyze)

    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!."

    return (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
