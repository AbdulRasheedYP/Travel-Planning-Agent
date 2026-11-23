
from .document_loader import load_document
from .chunking import chunk_text
from .embedding_service import generate_document_embedding
from .models import TravelKnowledge


def ingest_document(filename, destination):
    text = load_document(filename)
    chunks = chunk_text(text)

    clean_destination = destination.strip()

    # Remove previous chunks for this destination (case-insensitive)
    TravelKnowledge.objects.filter(
        destination__iexact=clean_destination
    ).delete()

    for chunk in chunks:
        embedding = generate_document_embedding(chunk)

        TravelKnowledge.objects.create(
            destination=clean_destination,
            content=chunk,
            embedding=embedding,
            source=filename,
        )

    return len(chunks)
