from pydantic import BaseModel, Field

class MovieCreate(BaseModel):
    title: str
    author: str
    rating: float = Field(..., ge=0, le=10)

class MovieResponse(MovieCreate):
    id: str