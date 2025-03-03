# AI model prompting and logic module

import instructor
from pydantic import BaseModel, Field
from openai import OpenAI
from config import settings
from typing import List
#from enum import Enum
import httpx
# some sample questions to classify
questions = settings.typical_questions





client = OpenAI(base_url=settings.base_url,
                api_key=settings.openrouter_api_key)
"""
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)
"""
completion = client.chat.completions.create(
  
  model="google/gemini-2.0-flash-exp:free",
  messages=[
    {
      "role": "user",
      "content": "Which tasks start on holiday?"    
    }
  ]
)
print(completion.choices[0].message.content)

"""
client = instructor.patch(client)

def classify_question(question_text: str) -> str:
    response = client.chat.completions.create(
        model=settings.default_model,
        messages=[
            {"role": "system", "content": "Classify the following project manager question into a category."},
            {"role": "user", "content": question_text}
        ]
    )
    return response.choices[0].message.content

result = classify_question(questions[0])
print(result)
"""