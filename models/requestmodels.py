from pydantic import BaseModel
from typing import Optional

class QuestionRequest(BaseModel):
    question: str
    context: Optional[str] = None 

class TextInput(BaseModel):
    text: str

class TextRequest(BaseModel):
    text: str
    max_length: int = 100  # Maximum length of the summary
    min_length: int = 30   # Minimum length of the summary