
from pgvector.django import CosineDistance

from .embedding_service import generate_query_embedding
from .models import TravelKnowledge


def retrieve_relevant_chunks(
    query,
    destination,
    top_k=3,
    max_distance=0.7,
):
    query_embedding = generate_query_embedding(query)

    results = (
        TravelKnowledge.objects
        .filter(destination__iexact=destination)
        .annotate(
            distance=CosineDistance(
                "embedding",
                query_embedding
            )
        )
        .filter(distance__lte=max_distance)
        .order_by("distance")[:top_k]
    )

    return list(results)
