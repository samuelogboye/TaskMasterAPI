from pydantic import BaseModel, Field, validator
from typing import Optional
import html
from datetime import datetime

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

    @validator('title', 'description')
    def sanitize_strings(cls, v):
        if v is None:
            return v
        return html.escape(v)

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True