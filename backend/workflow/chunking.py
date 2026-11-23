def chunk_text(text, chunk_size=500, overlap=100):
    if not text or not text.strip():
        return []

    sections = [s.strip() for s in text.split("\n\n") if s.strip()]
    chunks = []
    current_chunk = ""

    for section in sections:
        if current_chunk and len(current_chunk) + len(section) + 2 > chunk_size:
            chunks.append(current_chunk.strip())
            current_chunk = section
        else:
            if current_chunk:
                current_chunk += "\n\n" + section
            else:
                current_chunk = section

    if current_chunk and current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks