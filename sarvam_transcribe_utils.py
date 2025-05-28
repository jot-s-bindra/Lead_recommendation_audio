
import os
import time
from dotenv import load_dotenv
from sarvamai import SarvamAI

load_dotenv()

API_KEY = os.getenv("SARVAM_API_KEY")
if not API_KEY:
    raise ValueError("SARVAM_API_KEY not found in environment variables.")

sarvam_client = SarvamAI(api_subscription_key=API_KEY)

def transcribe_and_translate_sarvam(audio_path: str, source_lang: str = "hi-IN", target_lang: str = "en-IN") -> dict:
    """
    Transcribe audio and translate to English using Sarvam AI.

    Returns:
        dict with transcript, translated text and execution time.
    """
    start_time = time.perf_counter()

    with open(audio_path, "rb") as audio_file:
        stt = sarvam_client.speech_to_text.transcribe(
            file=audio_file,
            model="saarika:v2",
            language_code=source_lang
        )

    translation = sarvam_client.text.translate(
        input=stt.transcript,
        source_language_code=source_lang,
        target_language_code=target_lang
    )

    return {
        "transcript": stt.transcript,
        "translated_text": translation.translated_text,
        "execution_time_sec": round(time.perf_counter() - start_time, 2)
    }
