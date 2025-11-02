"""
Configuration management for VC Council
Loads environment variables and validates settings
"""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings from environment variables"""

    # LLM Configuration
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    llm_provider: str = "openai"
    llm_model: str = "gpt-4-turbo-preview"

    # Metorial Configuration
    metorial_api_key: Optional[str] = "placeholder"
    metorial_base_url: str = "https://api.metorial.com/v1"

    # MCP Deployment IDs
    mcp_apify_id: Optional[str] = "placeholder"
    mcp_github_id: Optional[str] = "placeholder"
    mcp_hackernews_id: Optional[str] = "placeholder"
    mcp_gdrive_id: Optional[str] = "placeholder"
    mcp_gcalendar_id: Optional[str] = "placeholder"

    # Backend Configuration
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000

    # CORS
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    model_config = ConfigDict(
        env_file=".env",  # Load from backend/.env
        case_sensitive=False
    )

    def validate_llm_config(self):
        """Ensure at least one LLM provider is configured"""
        if self.llm_provider == "openai" and not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when using OpenAI")
        if self.llm_provider == "anthropic" and not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is required when using Anthropic")

# Global settings instance
settings = Settings()
# TODO: Uncomment when you have real API keys
# settings.validate_llm_config()
