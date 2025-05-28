from recommendation_utils import recommend_from_text

def test_recommendation():
    query = "Looking for a Hindi-speaking person interested in home loans"
    results = recommend_from_text(query, language="Hindi")
    
    assert isinstance(results, list), "Recommendation result is not a list"
    
    print(f"\n✅ test_recommendation passed with {len(results)} results\n")
    for i, rec in enumerate(results, 1):
        print(f"--- Recommendation {i} ---")
        print(f"Score: {rec['score']}")
        print(f"Lead ID: {rec['lead_id']}")
        print(f"Name: {rec['contact']['name']}")
        print(f"Region: {rec['contact']['region']}")
        print(f"Language: {rec['contact']['preferred_language']}")
        print(f"Products: {', '.join(rec['interest']['products'])}")
        print(f"Notes: {rec['notes']}\n")

test_recommendation()
