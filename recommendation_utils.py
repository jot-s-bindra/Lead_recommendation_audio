
from typing import List, Dict
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, MatchAny
from qdrant_utils import client
from embedding_utils import get_openai_embedding

def recommend_from_text(
    search_text: str,
    language: str = None,
    products: List[str] = None,
    limit: int = 5,
    use_filters: bool = True  # NEW FLAG
) -> List[Dict]:
    """
    Find semantically similar leads using Qdrant vector search.

    Args:
        search_text (str): Query string.
        language (str, optional): Preferred language to filter.
        products (List[str], optional): List of product filters.
        limit (int): Number of leads to retrieve.
        use_filters (bool): Whether to apply filtering logic or not.

    Returns:
        List[Dict]: Top matching leads.
    """
    vector = get_openai_embedding(search_text)

    # Only apply filters if use_filters is True
    query_filter = None
    if use_filters:
        conditions = []
        if language:
            conditions.append(FieldCondition(
                key="contact.preferred_language",
                match=MatchValue(value=language)
            ))
        if products:
            conditions.append(FieldCondition(
                key="interest.products",
                match=MatchAny(any=products)
            ))
        if conditions:
            query_filter = Filter(must=conditions)

    results = client.search(
        collection_name="gromo_leads",
        query_vector=vector,
        limit=limit,
        with_payload=True,
        query_filter=query_filter
    )

    return [{
        "score": round(point.score, 3),
        **point.payload
    } for point in results]
