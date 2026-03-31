import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from algorithms import astar_search, depth_limited_search, greedy_best_first_search, uniform_cost_search
from map import Map

ALGORITHMS = {
    "ucs": uniform_cost_search,
    "dls": depth_limited_search,
    "greedy": greedy_best_first_search,
    "astar": astar_search
}

app = FastAPI()

# Allowed origins
origins = [
    "http://localhost:5173", # Vue frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/graph")
def default_graph():
    with open("data/map.json") as f:
        return json.load(f)

class SearchRequest(BaseModel):
    map_json: dict
    start: str
    goal: str
    algorithm: str
    depth: int = 10
    heuristic: dict = {}

class SearchResponse(BaseModel):
    status: str
    cost: float | None
    path: list    


@app.post("/api/search")
def search(req: SearchRequest):
    m = Map.from_json(req.map_json)

    algorithm = ALGORITHMS.get(req.algorithm)

    if not algorithm:
        raise HTTPException(400, "Unknown algorithm")

    result = algorithm(
        m,
        req.start,
        req.goal,
        heuristic=req.heuristic,
        depth=req.depth
    )

    return SearchResponse(status=result[0], cost=result[1], path=result[2])