import json
from algorithms import uniform_cost_search
from map import Map

with open("map.json") as f:
    data = json.load(f)

m = Map()

for city, neighbors in data.items():
    for neighbor, dist in neighbors.items():
        m.add_edge(city, neighbor, dist)
""" 
for city, neighbors in m.edges.items():
    print(f"{city}: {neighbors}")
""" 

cost, path = uniform_cost_search(m, "Aveiro", "Faro") 

print(f"Cost: {cost}")
print(f"Path: {path}")

""" 
with open("heuristic.json") as f:
    data = json.load(f)

for city, heuristic in data.items():
    print(f"{city}: {heuristic}")
"""