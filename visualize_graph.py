import networkx as nx
import matplotlib.pyplot as plt


def visualize_graph(map_obj):
    """
    Visualizes the map graph using NetworkX and Matplotlib.

    Each city is represented as a node and each road between cities
    is represented as an edge with the corresponding distance.

    Parameters
    ----------
    map_obj : Map
        Instance of the Map class containing the graph stored as an
        adjacency list (map_obj.edges).
    """

    # Create an empty undirected graph
    G = nx.Graph()

    # Add edges and weights from the Map adjacency list
    # map_obj.edges structure:
    # { city: {neighbor_city: distance} }
    for city, neighbors in map_obj.edges.items():
        for neighbor, dist in neighbors.items():
            if not G.has_edge(city, neighbor):
                G.add_edge(city, neighbor, weight=dist)

    # Compute positions for nodes using a force-directed layout
    # This spreads nodes out in a visually pleasant way
    pos = nx.spring_layout(G)

    # Draw the nodes and edges of the graph
    nx.draw(
        G,
        pos,
        with_labels=True,      # Show city names
        node_color="lightblue",
        node_size=2000,
        font_size=10
    )

    # Extract edge weights to display as labels
    edge_labels = nx.get_edge_attributes(G, "weight")

    # Draw the distance labels on each edge
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels
    )

    # Display the graph window
    plt.show()

