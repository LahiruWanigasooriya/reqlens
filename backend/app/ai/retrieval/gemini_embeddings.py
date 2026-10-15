from typing import Any

from google import genai
from llama_index.core.embeddings import BaseEmbedding

from app.core.config import settings


class GeminiEmbedding(BaseEmbedding):

    model_name: str = settings.EMBEDDING_MODEL

    def __init__(
        self,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)

        self._client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def _embed(
        self,
        text: str,
        task_type: str,
    ) -> list[float]:

        result = self._client.models.embed_content(
            model=self.model_name,
            contents=text,
            config={
                "task_type": task_type,
                "output_dimensionality":
                    settings.EMBEDDING_DIMENSIONS,
            },
        )

        return list(
            result.embeddings[0].values
        )

    def _get_query_embedding(
        self,
        query: str,
    ) -> list[float]:

        return self._embed(
            query,
            "RETRIEVAL_QUERY",
        )

    async def _aget_query_embedding(
        self,
        query: str,
    ) -> list[float]:

        return self._get_query_embedding(
            query
        )

    def _get_text_embedding(
        self,
        text: str,
    ) -> list[float]:

        return self._embed(
            text,
            "RETRIEVAL_DOCUMENT",
        )