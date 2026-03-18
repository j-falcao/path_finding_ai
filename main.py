import json
from algorithms import depth_limited_search, uniform_cost_search
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

# TESTES

# uniform_cost_search
""" 
cost, path = uniform_cost_search(m, "Aveiro", "Faro") 

print(f"Cost: {cost}")
print(f"Path: {path}") 
"""

# depth_limited_search
""" 
status, cost, path = depth_limited_search(m, "Lisboa", "Porto", limit=3)

print(f"Status : {status}")
print(f"Cost   : {cost} km")
print(f"Path   : {' → '.join(path)}")
""" 



# HEURISTIC

""" 
with open("heuristic.json") as f:
    data = json.load(f)

for city, heuristic in data.items():
    print(f"{city}: {heuristic}")
"""