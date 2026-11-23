import logging
from pgvector.django import CosineDistance

from .embedding_service import generate_query_embedding
from .models import TravelKnowledge

logger = logging.getLogger(__name__)


def retrieve_relevant_chunks(
    query,
    destination,
    top_k=3,
    max_distance=0.7,
):
    try:
        clean_destination = destination.strip() if destination else ""
        if not clean_destination:
            return []

        # Find knowledge for this destination
        # 1. Exact match (case-insensitive)
        base_qs = TravelKnowledge.objects.filter(destination__iexact=clean_destination)

        # 2. If no exact match and user provided "City, State/Country" (e.g. "Munnar, Kerala")
        if not base_qs.exists() and "," in clean_destination:
            primary_dest = clean_destination.split(",")[0].strip()
            base_qs = TravelKnowledge.objects.filter(destination__iexact=primary_dest)

        # 3. Fallback to contains match if still no direct match
        if not base_qs.exists():
            base_qs = TravelKnowledge.objects.filter(destination__icontains=clean_destination)

        if not base_qs.exists():
            return []

        query_embedding = generate_query_embedding(query)

        results = (
            base_qs
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

    except Exception as error:
        logger.error(f"Error in retrieve_relevant_chunks: {error}", exc_info=True)
        return []
