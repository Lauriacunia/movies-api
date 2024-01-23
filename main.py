import stat
from urllib import response
from fastapi import Depends, FastAPI, Query , Body, Path, Query
from movies import movies , Movie
from users import User
from fastapi.responses import HTMLResponse, JSONResponse 
from typing import List 
from jwt_manager import create_access_token, decode_access_token, JWTBearer
from config import settings


app = FastAPI()

#Auth
@app.post("/login", tags=["Auth"])
def login(user: User):
    if user.email == "admin@admin" and user.password == "admin":
        access_token = create_access_token(data={"email": user.email})
        return {"access_token": access_token}
    return {"error": "Invalid credentials"}

@app.get("/", tags=["Root"])
def root():
    return {"message": "Hello World"}

@app.get("/movies", tags=["Movies"], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_movies(
    year: int = Query(None, description="Optional parameter to filter movies by year",
                       le=2024, gt=1900) )-> List[Movie]:
    if year:
        filtered_movies = [movie for movie in movies if movie["year"] == year]
        return filtered_movies
    return movies

@app.get("/movies/{movie_id}", tags=["Movies"], response_model=Movie)
def get_movie(movie_id: int = Path(gt=0, description="The ID of the movie to get")):
    movie = next((movie for movie in movies if movie["id"] == movie_id), None)
    if movie:
        return JSONResponse(content=movie)
    return JSONResponse(content={"error": "Movie with id: {} not found".format(movie_id)}, status_code=404)

@app.post("/movies", tags=["Movies"], status_code=201, response_model= dict)
def add_movie(movie: Movie = Body(..., embed=True)) -> dict:
    if not movie:
        return {"error": "No movie provided."}
    #crea una copia de movie y agragle el nuevo id
    movie = movie.model_dump()
    movie["id"] = len(movies) + 1
    movies.append(movie)
    return {"message": "Movie created.",
            "movie": movie}

@app.put("/movies/{movie_id}", tags=["Movies"], response_model= dict)
def update_movie(movie_id: int, new_movie: Movie) -> dict:
    movie = next((movie for movie in movies if movie["id"] == movie_id), None)
    if not movie:
        return {"error": "No movie found."}
    movie["name"] = new_movie.name
    movie["description"] = new_movie.description
    movie["cast"] = new_movie.cast
    movie["year"] = new_movie.year
    return movie

@app.delete("/movies/{movie_id}", tags=["Movies"])
def delete_movie(movie_id: int):
    movie = next((movie for movie in movies if movie["id"] == movie_id), None)
    if movie:
      movies.remove(movie)
      return {"message": "Movie with id: {} deleted".format(movie_id)}
    return {"message": "Movie with id: {} not found".format(movie_id)}


