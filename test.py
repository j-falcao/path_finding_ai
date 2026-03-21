import networkx as nx

def to_networkx(map_obj):
    G = nx.Graph()

    for city, neighbors in map_obj.edges.items():
        for neighbor, dist in neighbors.items():
            G.add_edge(city, neighbor, weight=dist)

    return G



import matplotlib.pyplot as plt
import json
from map import Map

with open("data/map.json") as f:
    data = json.load(f)

m = Map()

for city, neighbors in data.items():
    for neighbor, dist in neighbors.items():
        m.add_edge(city, neighbor, dist)

G = to_networkx(m)

pos = nx.spring_layout(G)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="lightblue",
    node_size=2000,
    font_size=10
)

edge_labels = nx.get_edge_attributes(G, "weight")

nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.show()

