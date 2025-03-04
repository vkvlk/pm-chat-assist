
import instructor
from pydantic import BaseModel
from openai import OpenAI
from config import settings
from llm import LLMResponse



# Patch the OpenAI client
client = instructor.from_openai(OpenAI(base_url=settings.base_url, api_key=settings.openrouter_api_key), mode=instructor.Mode.JSON)

# Extract structured data from natural language
res = client.chat.completions.create(
    model=settings.default_model,
    temperature=settings.temperature,
    max_tokens=settings.max_tokens/2,
    response_model=LLMResponse,
    max_retries=3,
    messages=[{"role": "user", "content": "Need to analyze some tasks with holidays impact."}],
)

#assert res.name == "John Doe"
#assert res.age == 30

print(res.model_dump_json())  # IT WORKS! 