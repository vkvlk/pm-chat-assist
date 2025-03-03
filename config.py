from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    openrouter_api_key: str = Field(..., env="OPENROUTER_API_KEY")
    base_url: str = "https://api.openrouter.io/v1/"
    default_model: str = "google/gemini-2.0-flash-exp:free"
    temperature: float = 0.3
    max_tokens: int = 2000

    data_file_path: str = "data.xlsx"
    country_code: str = "US"
    default_years: List[int] = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
    typical_questions: List[str] = ["Which tasks start on holiday?",
                                    "Which tasks are impacted by July 4th?",
                                    "How many days we prolong project delivery if no task can be completed during the weekend?"]





    class Config:
        env_file = ".env"
        arbitrary_types_allowed = True

settings = Settings()