from networkx import nx
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
    G = nx.read_gml('data/map.gml')

    # Nodes
    nodes = [{'data': {'id': str(n), 'label': str(n)}} for n in G.nodes()]

    # Edges with weight
    edges = []
    for u, v, attr in G.edges(data=True):
        edges.append({
            'data': {
                'id': f"{u}-{v}",
                'source': str(u),
                'target': str(v),
                'weight': attr.get('weight', 1)  # default to 1 if missing
            }
        })

    cy_data = {'nodes': nodes, 'edges': edges}
    return cy_data



class SearchRequest(BaseModel):
    gml_data: str
    start: str
    goal: str
    algorithm: str
    depth: int = 10


@app.post("/api/search")
def search(req: SearchRequest):
    m = Map.from_gml(req.gml_data)

    algorithm = ALGORITHMS.get(req.algorithm)

    if not algorithm:
        raise HTTPException(400, "Unknown algorithm")

    return algorithm(
        m,
        req.start,
        req.goal,
        heuristic=req.heuristic,
        depth=req.depth
    )
