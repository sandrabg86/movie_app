from pydantic import BaseModel, Field

class Movie(BaseModel):
    title: str
    author: str
    rating: float = Field(..., ge=0, le=10)