# AI model prompting and logic module

import instructor
from pydantic import BaseModel, Field
from openai import OpenAI
from config import settings

from typing import List
from enum import Enum


questions = settings.typical_questions


client = OpenAI(api_key=settings.openrouter_api_key,
                base_url=settings.base_url,)

