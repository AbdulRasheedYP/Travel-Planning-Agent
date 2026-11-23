from pathlib import Path


KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"


def load_document(filename):
    file_path = KNOWLEDGE_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return text