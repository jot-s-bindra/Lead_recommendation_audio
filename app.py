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
        recommendations = recommend_from_text(translated_text, use_filters=False)

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
@app.route("/gp-profile-recommend", methods=["POST"])
def gp_profile_recommend():
    try:
        profile = request.get_json()
        if not profile:
            return jsonify({"error": "Missing GP profile in JSON"}), 400

        language = profile.get("language_preferred")
        profile_notes = profile.get("profile_notes", "")
        product_scores = profile.get("conversion_rates_by_product", {})

        # Select top products (you can change logic to threshold or top-N)
        top_products = sorted(product_scores, key=product_scores.get, reverse=True)[:2]

        recommendations = recommend_from_text(
            search_text=profile_notes,
            language=language,
            products=top_products,
            use_filters=True
        )


        return jsonify({
            "gp_id": profile.get("_id"),
            "used_language_filter": language,
            "used_product_filters": top_products,
            "recommendations": recommendations
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
