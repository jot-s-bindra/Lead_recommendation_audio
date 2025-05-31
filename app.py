import os
import time
from flask import Flask, request, jsonify
from sarvam_transcribe_utils import transcribe_and_translate_sarvam
from recommendation_utils import recommend_from_text
from mongo_utils import get_gp_profile_by_id
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
        transcribe_result = transcribe_and_translate_sarvam(filename, source_lang=language)
        translated_text = transcribe_result["translated_text"]

        recommendations = recommend_from_text(translated_text, use_filters=False)

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

@app.route("/gp-profile-recommend", methods=["POST"])
def gp_profile_recommend():
    try:
        data = request.get_json()
        if not data or "gp_id" not in data:
            return jsonify({"error": "Missing 'gp_id' in JSON"}), 400

        gp_id = data["gp_id"]
        profile = get_gp_profile_by_id(gp_id)

        language = profile.get("language_preferred")
        profile_notes = profile.get("dashboard", {}).get("positive_points", "")
        ## add courses done by him also if which gp did what is known add to context
        contxtt=language +" "+ profile_notes
        print(contxtt)
        recommendations = recommend_from_text(
            search_text=profile_notes,
            language=language,
            products=None,         
            use_filters=False       
        )

        return jsonify({
            "gp_id": gp_id,
            "used_language_filter": language,
            "used_product_filters": None,
            "recommendations": recommendations
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/query-recommend", methods=["POST"])
def query_recommend():
    try:
        data = request.get_json()
        if not data or "query" not in data:
            return jsonify({"error": "Missing 'query' in JSON"}), 400

        query_text = data["query"]
        recommendations = recommend_from_text(
            search_text=query_text,
            language=None,
            products=None,
            use_filters=False
        )

        return jsonify({
            "query": query_text,
            "recommendations": recommendations
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
