# AI model prompting and logic module

import instructor
from pydantic import BaseModel, Field
from openai import OpenAI
from config import settings
from typing import List, Literal, Optional, Dict
from models import TaskAnalysisRequest
from dataset import load_and_format_data
from enum import Enum



client = OpenAI(base_url=settings.base_url,
                api_key=settings.openrouter_api_key)


class LLMResponse(BaseModel):
    """Model for structured LLM responses"""
    response_type: Literal["task_analysis", "schedule_impact", "general_query"]
    content: str
    confidence: float = Field(ge=0.0, le=1.0)
    relevant_tasks: Optional[List[str]] = Field(default_factory=list)
    date_range: Optional[Dict[str, str]] = None  # Changed datetime to str for compatibility

def llm_query(question_text: str, data: Optional[str]=" ") -> LLMResponse:
    try:    
        patched_client = instructor.patch(client, mode=instructor.Mode.MD_JSON)
        # Get structured response using Instructor
        response = patched_client.chat.completions.create(
            model=settings.default_model,
            temperature=settings.temperature,
            # max_tokens=settings.max_tokens,
            max_retries=3,
            response_model=LLMResponse,
            messages=[
                {"role": "system", "content": settings.SYSTEM_PROMPT + (data+"")},
                {"role": "user", "content": question_text}
            ]
        )
        
        # With instructor, response is already the LLMResponse object
        # Format the response for display
        formatted_response = response.content
        if response.relevant_tasks:
            formatted_response += "\n\nRelevant Tasks:\n" + "\n".join(response.relevant_tasks)
        if response.date_range:
            formatted_response += f"\n\nDate Range: {response.date_range['start']} to {response.date_range['end']}"
        
        return formatted_response
        
    except Exception as e:
        return f"An error occurred: {e}"

