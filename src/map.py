class Map:
    """
    Class that represents a map as a graph using an adjacency list.
    Each city is a node and each road between cities is an edge with a distance.
    """

    def __init__(self):
        # Dictionary that stores the graph
        # Structure: {city: {neighbor_city: distance}}
        self.edges = {}

    def add_city(self, city):
        """
        Adds a new city (node) to the graph.

        If the city already exists, nothing happens.
        """
        if city not in self.edges:
            # Initialize the city with an empty dictionary of neighbors
            self.edges[city] = {}

    def add_edge(self, city1, city2, distance):
        """
        Adds a bidirectional edge between two cities with a given distance.

        Parameters:
        city1 (str): First city
        city2 (str): Second city
        distance (int): Distance between the cities
        """

        # Ensure both cities exist in the graph
        self.add_city(city1)
        self.add_city(city2)

        # Add the connection from city1 to city2
        self.edges[city1][city2] = distance

        # Add the reverse connection since roads are bidirectional
        self.edges[city2][city1] = distance

    def neighbors(self, city):
        """
        Returns all neighboring cities and distances for a given city.

        Parameters:
        city (str): City whose neighbors we want

        Returns:
        dict: Dictionary of neighbors and their distances
        """
        return self.edges[city]
