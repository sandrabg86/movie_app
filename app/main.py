from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI()

client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client.movie_db
collection = db.movies

class MovieModel(BaseModel):
    title: str
    author: str
    rating: float = Field(..., ge=0, le=10)

class MovieDB(MovieModel):
    id: str

@app.post("/movies/", response_model=MovieDB)
async def create_movie(movie: MovieModel):
    movie_doc = movie.dict()
    result = await collection.insert_one(movie_doc)
    return MovieDB(id=str(result.inserted_id), **movie_doc)

@app.get("/movies/", response_model=List[MovieDB])
async def list_movies():
    movies = await collection.find().to_list(1000)
    return [MovieDB(id=str(movie["_id"]), **movie) for movie in movies]

@app.get("/movies/{id}", response_model=MovieDB)
async def get_movie(id: str):
    movie = await collection.find_one({"_id": ObjectId(id)})
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return MovieDB(id=str(movie["_id"]), **movie)

@app.put("/movies/{id}", response_model=MovieDB)
async def update_movie(id: str, movie: MovieModel):
    result = await collection.update_one({"_id": ObjectId(id)}, {"$set": movie.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie = await collection.find_one({"_id": ObjectId(id)})
    return MovieDB(id=str(movie["_id"]), **movie)

@app.delete("/movies/{id}")
async def delete_movie(id: str):
    result = await collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}