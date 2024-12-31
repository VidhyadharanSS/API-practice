from fastapi import FastAPI, Path
from  pydantic import BaseModel
from typing import Optional

app = FastAPI()

movies = {
    1:{
        "name" : "Dune 1",
        "year" : 2021
    },
    2:{
        "name" : "Dune 2",
        "year" : 2024
    }
}

class Movies(BaseModel):
    name: str
    year: int

class UpdateMovies(BaseModel):
    name: Optional[str] = None
    year: Optional[int] = None

@app.get('/get-all-movies')
def get_all_movies():
    return movies

@app.get('/get-movies-by-id/{movie_id}')
def get_movies_by_id(movie_id: int = Path(description = "I will list your movies", gt = 0, lt = 3)):
    return movies[movie_id]

@app.get('/api/get-movies-by-name/{movie_id}')
def get_movies_by_name(*, movie_id: int, movie_name: Optional[str] = None):
    for movie_id in movies:
        if movies[movie_id]['name'] == movie_name:
            return movies[movie_id]
    return {"Data": "Not found"}

@app.post('/api/create-movie/{movie_id}')
def create_movie(*, movie_id: int = Path(description = "New movie added", lt = 10), movie : Movies):
    if movie_id in movies:
        return {'Error': 'Movie already exists'}
    else:
        movies[movie_id] = movie
        return movies[movie_id]


@app.put('/api/update-movie/{movie_id}')
def update_movie(*, movie_id: int, movie : UpdateMovies):
    if movie_id not in movies:
        return {'Error' : 'Movie doesnt exist'}
    else:
        if movie.name != None:
            movies[movie_id]['name'] = movie.name
        if movie.year != None:
            movies[movie_id]['year'] = movie.year

    return movies[movie_id]
        
@app.delete('/api/delete-movie/{movie_id}')
def delete_movie(*, movie_id: int):
    if movie_id not in movies:
        return {'Error' : 'Movie doesnt exist'}
    del movies[movie_id]
