from sarvam_transcribe_utils import transcribe_and_translate_sarvam

def test_transcription():
    result = transcribe_and_translate_sarvam("/home/outbreakkp/testleadrecom.mp3", source_lang="hi-IN")
    
    assert "transcript" in result and "translated_text" in result, "Missing expected keys"
    
    print("\n✅ test_transcription passed!")
    print(f"📝 Transcript: {result['transcript']}")
    print(f"🌐 Translated Text: {result['translated_text']}")
    print(f"⏱️ Execution Time: {result['execution_time_sec']} sec\n")

test_transcription()
