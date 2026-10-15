import uuid

from llama_index.core import (
    VectorStoreIndex,
)
from llama_index.core.schema import (
    QueryBundle,
)

from app.ai.retrieval.gemini_embeddings import (
    GeminiEmbedding,
)
from app.ai.retrieval.vector_store import (
    get_project_vector_store,
)
from app.core.config import settings


def retrieve_project_evidence(
    project_id: uuid.UUID,
    query: str,
    top_k: int | None = None,
    evidence_types: list[str] | None = None,
):

    embed_model = GeminiEmbedding()

    vector_store = (
        get_project_vector_store(
            str(project_id)
        )
    )

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=embed_model,
    )

    retriever = index.as_retriever(
        similarity_top_k=(
            top_k
            or settings.RETRIEVAL_TOP_K
        )
    )

    nodes = retriever.retrieve(
        QueryBundle(query_str=query)
    )

    results = []

    for result in nodes:

        metadata = (
            result.node.metadata
            or {}
        )

        evidence_type = (
            metadata.get(
                "evidence_type"
            )
        )

        if (
            evidence_types
            and evidence_type
            not in evidence_types
        ):
            continue

        results.append(
            {
                "vector_id":
                    result.node.node_id,

                "score":
                    float(
                        result.score or 0
                    ),

                "content":
                    result.node.get_content(
                        metadata_mode="none"
                    ),

                "source_name":
                    metadata.get(
                        "source_name"
                    ),

                "evidence_type":
                    evidence_type,

                "project_file_id":
                    metadata.get(
                        "project_file_id"
                    ),

                "chunk_index":
                    metadata.get(
                        "chunk_index"
                    ),
            }
        )

    return results