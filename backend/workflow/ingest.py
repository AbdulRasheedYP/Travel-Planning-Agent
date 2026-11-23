
from .document_loader import load_document
from .chunking import chunk_text
from .embedding_service import generate_document_embedding
from .models import TravelKnowledge


def ingest_document(filename, destination):
    text = load_document(filename)
    chunks = chunk_text(text)

    # Remove previous chunks for this destination
    TravelKnowledge.objects.filter(
        destination=destination
    ).delete()

    for chunk in chunks:
        embedding = generate_document_embedding(chunk)

        TravelKnowledge.objects.create(
            destination=destination,
            content=chunk,
            embedding=embedding,
            source=filename,
        )

    return len(chunks)
