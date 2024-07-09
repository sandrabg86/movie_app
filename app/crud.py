from app.models import Movie
from app.database import get_database
from bson import ObjectId

db = get_database()

async def create_movie(movie: Movie):
    movie_doc = movie.dict()
    result = await db["movies"].insert_one(movie_doc)
    return str(result.inserted_id)

async def get_movies():
    movies = await db["movies"].find().to_list(1000)
    return movies

async def get_movie(id: str):
    movie = await db["movies"].find_one({"_id": ObjectId(id)})
    return movie

async def update_movie(id: str, movie: Movie):
    await db["movies"].update_one({"_id": ObjectId(id)}, {"$set": movie.dict()})
    updated_movie = await db["movies"].find_one({"_id": ObjectId(id)})
    return updated_movie

async def delete_movie(id: str):
    result = await db["movies"].delete_one({"_id": ObjectId(id)})
    return result.deleted_count