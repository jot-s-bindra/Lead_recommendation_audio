🔉 AUDIO-TO-RECOMMENDATION API

Endpoint:

POST http://127.0.0.1:5000/audio-to-recommend

Form Data:

    audio: Path to audio file (.mp3, .wav, etc.)

    language: Language code (e.g. hi-IN, en-IN)

Example:

curl -X POST http://127.0.0.1:5000/audio-to-recommend \
  -F "audio=@/home/outbreakkp/testleadrecom.mp3" \
  -F "language=hi-IN"

Expected JSON Response:

{
  "transcription": "<Original transcript>",
  "translated_text": "<Translated English text>",
  "execution_time_sec": 2.94,
  "recommendations": [
    {
      "score": 0.912,
      "contact": {...},
      "interest": {...},
      "notes": "...",
      ...
    }
  ]
}

👤 GP PROFILE-TO-RECOMMENDATION API

Endpoint:

POST http://127.0.0.1:5000/gp-profile-recommend

Headers:

Content-Type: application/json

Body (JSON):

{
  "_id": "GP123",
  "name": "Akshay Kumar",
  "language_preferred": "Hindi",
  "conversion_rates_by_product": {
    "home_loan": 0.38,
    "credit_card": 0.52
  },
  "profile_notes": "Good with budget-conscious clients and home loan conversions."
}

Example:

curl -X POST http://127.0.0.1:5000/gp-profile-recommend \
  -H "Content-Type: application/json" \
  -d '{
    "_id": "GP123",
    "name": "Akshay Kumar",
    "language_preferred": "Hindi",
    "conversion_rates_by_product": {
      "home_loan": 0.38,
      "credit_card": 0.52
    },
    "profile_notes": "Good with budget-conscious clients and home loan conversions."
  }'

Expected JSON Response:

{
  "query_text": "Good with budget-conscious clients and home loan conversions.",
  "filters": {
    "language": "Hindi",
    "products": ["home_loan", "credit_card"]
  },
  "recommendations": [
    {
      "score": 0.874,
      "contact": {...},
      "interest": {...},
      "notes": "...",
      ...
    }
  ]
}
