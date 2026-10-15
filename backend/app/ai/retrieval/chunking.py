from llama_index.core.node_parser import (
    SentenceSplitter,
)

from app.core.config import settings


splitter = SentenceSplitter(
    chunk_size=settings.KNOWLEDGE_CHUNK_SIZE,
    chunk_overlap=settings.KNOWLEDGE_CHUNK_OVERLAP,
)


def split_content(
    content: str,
) -> list[str]:

    chunks = splitter.split_text(
        content
    )

    return [
        chunk.strip()
        for chunk in chunks
        if chunk.strip()
    ]