from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

import services

app = FastAPI()


class SearchMovie(BaseModel):
    query: str


class SearchOneMovie(BaseModel):
    movieName: str
    langs: Union[list[str], None] = None


class MovieDownloadLink(BaseModel):
    movie: str
    lang: Union[str, None] = None
    id: int


@app.post(
    "/"
)
async def get_all_movies(data: SearchMovie):
    return await services.get_all_movies(data.model_dump())


@app.post("/one-movie/")
async def get_one_movie(data: SearchOneMovie):
    return await services.get_one_movie(data.model_dump())


@app.post("/download-subtitle/")
async def get_download_movie_subtitle(data: MovieDownloadLink):
    return await services.get_download_movie_page(data.model_dump())


@app.post("/search/")
async def search_subtitle(data: SearchMovie):
    return await services.search_for_subtitle(data.model_dump()["query"])
