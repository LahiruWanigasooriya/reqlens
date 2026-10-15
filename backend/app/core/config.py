from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "ReqLens"
    APP_ENV: str = "development"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str

    FRONTEND_URL: str = "http://localhost:3000"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    UPLOAD_DIR: str = "storage/uploads"
    MAX_UPLOAD_SIZE_MB: int = 20

    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"

    CHROMA_DIR: str = "storage/chroma"
    EMBEDDING_MODEL: str = "gemini-embedding-001"
    EMBEDDING_DIMENSIONS: int = 768

    KNOWLEDGE_CHUNK_SIZE: int = 800
    KNOWLEDGE_CHUNK_OVERLAP: int = 120

    RETRIEVAL_TOP_K: int = 8

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()