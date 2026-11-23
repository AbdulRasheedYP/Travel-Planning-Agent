import os

from google import genai

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

EMBEDDING_MODEL = "gemini-embedding-001"


def generate_embedding(text):
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
    )

    return response.embeddings[0].values