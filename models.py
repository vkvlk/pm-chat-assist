# try ro separete the models with logic from the main app

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal
from datetime import datetime




class Task(BaseModel):
    """Model representing a project task"""
    id: str
    name: str
    start_date: datetime
    end_date: datetime
    duration: int
    predecessors: Optional[List[str]] = None
    successors: Optional[List[str]] = None

