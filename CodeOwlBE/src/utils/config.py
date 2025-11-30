from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application configuration loaded from environment variables"""

    model_config: SettingsConfigDict = SettingsConfigDict(env_file=".env", extra="allow") 
    # GitHub Configuration
    github_webhook_secret: str = Field(default="test")
    github_app_id: str = Field(default="123")
    github_app_private_key_path: str = Field(default="./key.pem")
    github_installation_id: str = Field(default="123")

    # AI Configuration
    gemini_api_key: str

    # Qdrant Configuration
    qdrant_host: str = Field(default="localhost")
    qdrant_port: int = Field(default=6333)

    # Embedding Configuration
    embedding_model: str = Field(default="BAAI/bge-small-en-v1.5")
    embedding_dimension: int = Field(default=384)

    '''
    class Config:
        env_file = ".env"
    '''

settings = Settings()