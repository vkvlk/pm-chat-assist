from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    openrouter_api_key: str = Field(..., env="OPENROUTER_API_KEY")
    default_model: str = "google/gemini-2.0-flash-exp:free"
    data_file_path: str = "data.xlsx"
    country_code: str = "US"

    class Config:
        env_file = ".env"
        arbitrary_types_allowed = True

settings = Settings()