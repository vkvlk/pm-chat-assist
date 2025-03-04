# AI model prompting and logic module

import instructor
from pydantic import BaseModel, Field
from openai import OpenAI
from config import settings
from typing import List, Literal, Optional, Dict
from dataset import load_data

# Define the LLM response model
class LLMResponse(BaseModel):
    """Model for structured LLM responses"""
    response_type: Literal["task_analysis", "holiday_impact", "weekend_impact", "schedule_impact", "path_analysis", "general_query"]
    content: str
    confidence: float = Field(ge=0.0, le=1.0)
    relevant_tasks: Optional[List[str]] = Field(default_factory=list)
    date_range: Optional[Dict[str, str]] = None  # Changed datetime to str for compatibility    

# Define the LLM query function
def llm_query(question_text: str, data: Optional[str]=" ") -> LLMResponse:
    try:    
        # Create a new client with the current API key
        client = OpenAI(
            base_url=settings.base_url,
            api_key=settings.openrouter_api_key,
        )
    
        patched_client = instructor.from_openai(client, mode=instructor.Mode.JSON)
        
        # Ensure data is properly formatted
        system_content = settings.TEST_PROMPT
        #system_content = "You are project manager assistent, helping with project schedule and maintain tasks"
        #if data and isinstance(data, str):
         #   system_content += str(data)
        
        response = patched_client.chat.completions.create(
            model=settings.default_model,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
            max_retries=2,
            response_model=LLMResponse,
            messages=[
                {"role": "system", "content": system_content + data},
                {"role": "user", "content": question_text}
            ]
        )
        
        # response is already a LLMResponse object ready to .model_dump_json()
        return response
        
    except Exception as e:
        error_msg = str(e)
        # Add more detailed error information
        if "'NoneType' object is not subscriptable" in error_msg:
            error_msg += " - This typically happens when the API response is incomplete (Openrouter error)"
            
        # Always return a LLMResponse object, even for errors
        return LLMResponse(
            response_type="error_msg",
            content=f"Error processing request: {error_msg}",
            confidence=0.0,
            relevant_tasks=[],
            date_range=None
        )
