from pydantic import BaseModel
from typing import Optional

movies = [
    {
        "id": 1,
        "name": "Inception",
        "description": "A mind-bending heist film",
        "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ellen Page"],
        "year": 2010
    },
    {
        "id": 2,
        "name": "The Shawshank Redemption",
        "description": "A tale of hope and perseverance",
        "cast": ["Tim Robbins", "Morgan Freeman"],
        "year": 1994
    },
    {
        "id": 3,
        "name": "The Dark Knight",
        "description": "A superhero crime thriller",
        "cast": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
        "year": 2008
    },
    
]

class Movie(BaseModel):
    id: Optional[int]= None
    name: str
    description: str
    cast: list
    year: int

    class Config:
        schema_extra = {
            "example": {
                "name": "Inception",
                "description": "A mind-bending heist film",
                "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ellen Page"],
                "year": 2010
            }
        }