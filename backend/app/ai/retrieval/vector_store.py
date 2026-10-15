from pathlib import Path

import chromadb
from llama_index.vector_stores.chroma import (
    ChromaVectorStore,
)

from app.core.config import settings


def get_chroma_client():

    path = Path(
        settings.CHROMA_DIR
    )

    path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return chromadb.PersistentClient(
        path=str(path)
    )


def get_project_collection(
    project_id: str,
):

    client = get_chroma_client()

    collection_name = (
        "reqlens_"
        + project_id.replace("-", "_")
    )

    return client.get_or_create_collection(
        name=collection_name
    )


def get_project_vector_store(
    project_id: str,
):

    collection = (
        get_project_collection(
            project_id
        )
    )

    return ChromaVectorStore(
        chroma_collection=collection
    )


def clear_project_collection(
    project_id: str,
):

    client = get_chroma_client()

    collection_name = (
        "reqlens_"
        + project_id.replace("-", "_")
    )

    try:
        client.delete_collection(
            collection_name
        )
    except Exception:
        pass

    return client.get_or_create_collection(
        name=collection_name
    )