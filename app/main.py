from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

fake_movie_db = [
    {
        'name': 'my movie',
        'plot': 'my plot',
        'genres': ['Action', 'Adventure', 'Fantasy'],
        'casts': ['Tim', 'Kim', 'Fabian']
    }
]


class Movie(BaseModel):
    name: str
    plot: str
    genres: List[str]
    casts: List[str]


@app.get('/')
async def index():
    return {"Real": "Python"}


@app.post('/', status_code=201)
async def add_movie(payload: Movie):
    movie = payload.dict()
    fake_movie_db.append(movie)
    return {'id': len(fake_movie_db) - 1}


@app.put('/{id}')
async def update_movie(id: int, payload: Movie):
    movie = payload.dict()
    movies_length = len(fake_movie_db)
    if 0 <= id <= movies_length:
        fake_movie_db[id] = movie
        return None

    raise HTTPException(status_code=404, detail='Movie is not exists')
