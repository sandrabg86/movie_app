from fastapi import APIRouter, HTTPException
from app.schemas import MovieCreate, MovieResponse
from app import crud as crud_movie
from typing import List

router = APIRouter()

@router.post("/movies/", response_model=MovieResponse)
async def create_movie(movie: MovieCreate):
    movie_id = await crud_movie.create_movie(movie)
    return MovieResponse(id=movie_id, **movie.dict())

@router.get("/movies/", response_model=List[MovieResponse])
async def list_movies():
    movies = await crud_movie.get_movies()
    return [MovieResponse(id=str(movie["_id"]), **movie) for movie in movies]

@router.get("/movies/{id}", response_model=MovieResponse)
async def get_movie(id: str):
    movie = await crud_movie.get_movie(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return MovieResponse(id=str(movie["_id"]), **movie)

@router.put("/movies/{id}", response_model=MovieResponse)
async def update_movie(id: str, movie: MovieCreate):
    updated_movie = await crud_movie.update_movie(id, movie)
    if not updated_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return MovieResponse(id=str(updated_movie["_id"]), **updated_movie)

@router.delete("/movies/{id}")
async def delete_movie(id: str):
    deleted_count = await crud_movie.delete_movie(id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}