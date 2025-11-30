from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables"""

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    # GitHub Configuration
    github_token: str
    github_webhook_secret: str
    github_bot_token: str
    github_app_id: int
    github_app_slug: str
    github_app_private_key_path: str

    # AI Configuration
    gemini_api_key: str
    groq_api_key: str
    zai_api_key: str = ""
    ai_provider: str = "groq"

    # Qdrant Configuration
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333

    # Embedding Configuration
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    embedding_dimension: int = 384

    # Application Configuration
    temp_repo_dir: str = "./temp_repos"
    port: int = 8000


settings = Settings()
