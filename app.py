import os
import time
from flask import Flask, request, jsonify
from sarvam_transcribe_utils import transcribe_and_translate_sarvam
from recommendation_utils import recommend_from_text

app = Flask(__name__)

@app.route("/audio-to-recommend", methods=["POST"])
def audio_to_recommend():
    start_time = time.perf_counter()

    if 'audio' not in request.files:
        return jsonify({"error": "Missing audio file"}), 400

    audio_file = request.files['audio']
    language = request.form.get("language", "hi-IN")

    filename = audio_file.filename
    audio_file.save(filename)  # Save temporarily in the current directory

    try:
        # Step 1: Transcription + Translation
        transcribe_result = transcribe_and_translate_sarvam(filename, source_lang=language)
        translated_text = transcribe_result["translated_text"]

        # Step 2: Recommendation
        recommendations = recommend_from_text(translated_text, language=language)

        # Final response
        response = {
            "transcription": transcribe_result["transcript"],
            "translated_text": translated_text,
            "execution_time_sec": transcribe_result["execution_time_sec"],
            "recommendations": recommendations
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        total_time = round(time.perf_counter() - start_time, 2)
        print(f"🔄 Total API Execution Time: {total_time} seconds")

        # Clean up the audio file
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    app.run(debug=True)
