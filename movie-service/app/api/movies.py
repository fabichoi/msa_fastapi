from typing import List

from fastapi import APIRouter, HTTPException

import db_manager
from models import MovieOut, MovieIn, MovieUpdate
from service import is_cast_present

movies = APIRouter()


@movies.post('/', response_model=MovieOut, status_code=201)
async def create_movie(payload: MovieIn):
    for cast_id in payload.casts_id:
        if not is_cast_present(cast_id):
            raise HTTPException(status_code=404, detail=f'{cast_id} Case ID not found')

    movie_id = await db_manager.add_movie(payload)
    response = {
        'id': movie_id,
        **payload.dict()
    }
    return response


@movies.get('/', response_model=List[MovieOut])
async def get_movies():
    return await db_manager.get_movie(id)


@movies.get('/{id}/', response_model=MovieOut)
async def get_movies(id: int):
    movie = await db_manager.get_movie(id)
    if not movie:
        raise HTTPException(status_code=404, detail='Movie not found')
    return movie


@movies.put('/{id}', response_model=MovieOut)
async def update_movie(id: int, payload: MovieUpdate):
    movie = await db_manager.get_movie(id)
    if not movie:
        raise HTTPException(status_code=404, detail='Movie not found')

    update_data = payload.dict(exclude_unset=True)

    if 'casts_id' in update_data:
        for cast_id in payload.casts_id:
            if not is_cast_present(cast_id):
                raise HTTPException(status_code=404, detail=f'{cast_id} Case ID not found')

    movie_in_db = MovieIn(**movie)
    updated_movie = movie_in_db.copy(update=update_data)

    return await db_manager.update_movie(id, updated_movie)


@movies.delete('/{id}', response_model=None)
async def delete_movie(id: int):
    movie = await db_manager.get_movie(id)
    if not movie:
        raise HTTPException(status_code=404, detail='Movie not found')
    return await db_manager.delete_movie(id)
