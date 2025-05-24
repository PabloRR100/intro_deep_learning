# api.py
from fastapi import FastAPI, Query
from pydantic import BaseModel
import os 
import sys

script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'script'))
sys.path.append(script_path)
from similarity_template import PokemonSimilarity
import requests

app = FastAPI()

# Inicializa una vez el motor de similitud
similarity_engine = PokemonSimilarity()

@app.get("/")
async def root():
    return {"message": "Pokemon Similarity API"}

@app.post("/predict")
async def predict(img_url: str = Query(..., description="URL of the image to analyze")):
    try:
        closest_pokemon = similarity_engine.find_closest_pokemon(img_url)
        return {"closest_pokemon": closest_pokemon}
    except Exception as e:
        return {"error": str(e)}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
# api.py
