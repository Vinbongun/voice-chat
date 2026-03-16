from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PORT: int = 8000
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@postgres:5432/chat_db"

    # LLM
    OPENAI_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_BASE_URL: str = ""
    EMBED_MODEL: str = "text-embedding-3-small"

    # RAGFlow
    RAGFLOW_BASE_URL: str = "http://ragflow:9380"
    RAGFLOW_API_KEY: str = ""

    # Keycloak
    KEYCLOAK_URL: str = "https://keycloak.example.com"
    KEYCLOAK_REALM: str = "employees"
    KEYCLOAK_ADMIN_CLIENT_ID: str = "admin-cli"
    KEYCLOAK_ADMIN_CLIENT_SECRET: str = ""

    # Integrations
    BITRIX24_WEBHOOK_URL: str = ""
    ZUP_WEBSERVICE_URL: str = ""
    UIT_API_URL: str = ""
    UIT_API_TOKEN: str = ""

    # Observability
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_HOST: str = "http://langfuse:3000"

    # Development
    DEV_AUTH_BYPASS: bool = False  # Set to true in .env to skip JWT check


settings = Settings()
