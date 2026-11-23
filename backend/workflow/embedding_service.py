
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

EMBEDDING_MODEL = "gemini-embedding-001"


def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured")
    return genai.Client(api_key=api_key)


def generate_embedding(text, task_type):
    client = get_client()
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=3072,
        ),
    )

    return response.embeddings[0].values


def generate_document_embedding(text):
    return generate_embedding(text, "RETRIEVAL_DOCUMENT")


def generate_query_embedding(text):
    return generate_embedding(text, "RETRIEVAL_QUERY")
