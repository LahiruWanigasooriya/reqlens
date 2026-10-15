import uuid

from llama_index.core import (
    StorageContext,
    VectorStoreIndex,
)
from llama_index.core.schema import TextNode
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.ai.retrieval.chunking import (
    split_content,
)
from app.ai.retrieval.gemini_embeddings import (
    GeminiEmbedding,
)
from app.ai.retrieval.vector_store import (
    clear_project_collection,
    get_project_vector_store,
)
from app.models.knowledge_chunk import (
    KnowledgeChunk,
)
from app.models.project_file import ProjectFile


def build_project_knowledge_index(
    db: Session,
    project_id: uuid.UUID,
):

    files = db.scalars(
        select(ProjectFile).where(
            ProjectFile.project_id
            == project_id,

            ProjectFile.processing_status
            == "ready",
        )
    ).all()

    if not files:
        raise ValueError(
            "No processed project files found"
        )

    clear_project_collection(
        str(project_id)
    )

    db.execute(
        delete(KnowledgeChunk).where(
            KnowledgeChunk.project_id
            == project_id
        )
    )

    db.flush()

    nodes = []

    chunk_records = []

    for project_file in files:

        if not project_file.extracted_text:
            continue

        chunks = split_content(
            project_file.extracted_text
        )

        for index, content in enumerate(
            chunks
        ):

            vector_id = str(
                uuid.uuid4()
            )

            metadata = {
                "project_id":
                    str(project_id),

                "project_file_id":
                    str(project_file.id),

                "source_name":
                    project_file.original_name,

                "evidence_type":
                    project_file.evidence_type,

                "chunk_index":
                    index,
            }

            node = TextNode(
                id_=vector_id,
                text=content,
                metadata=metadata,
            )

            nodes.append(node)

            chunk_records.append(
                KnowledgeChunk(
                    project_id=project_id,

                    project_file_id=
                        project_file.id,

                    vector_id=vector_id,

                    chunk_index=index,

                    content=content,

                    evidence_type=
                        project_file.evidence_type,

                    source_name=
                        project_file.original_name,
                )
            )

    if not nodes:
        raise ValueError(
            "No indexable content found"
        )

    vector_store = (
        get_project_vector_store(
            str(project_id)
        )
    )

    storage_context = (
        StorageContext.from_defaults(
            vector_store=vector_store
        )
    )

    embed_model = GeminiEmbedding()

    VectorStoreIndex(
        nodes,
        storage_context=storage_context,
        embed_model=embed_model,
        show_progress=True,
    )

    db.add_all(
        chunk_records
    )

    db.commit()

    return {
        "files_indexed":
            len(
                {
                    chunk.project_file_id
                    for chunk
                    in chunk_records
                }
            ),

        "chunks_created":
            len(chunk_records),
    }