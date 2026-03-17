import heapq
from map import Map

def uniform_cost_search(map: Map, start: str, goal: str):
    """
    Finds the lowest-cost path between two cities using Uniform Cost Search.

    Parameters:
        map   (Map): Your Map instance with edges already populated
        start (str): Name of the starting city
        goal  (str): Name of the destination city

    Returns:
        A tuple (cost, path) where:
            cost (int | float): Total distance of the optimal path
            path (list[str])  : Ordered list of cities from start to goal
        Returns (inf, []) if no path exists.
    """

    # Priority queue entries: (cumulative_cost, current_city, path_so_far)
    heap = [(0, start, [start])]

    # Tracks the lowest cost at which each city was already finalized
    visited = {}

    while heap:
        cost, current, path = heapq.heappop(heap)

        # Skip if we've already found a cheaper route to this city
        if current in visited:
            continue

        # Mark city as finalized with its optimal cost
        visited[current] = cost

        # Goal check — we only verify on expansion, not on insertion,
        # so the cost is guaranteed to be optimal at this point
        if current == goal:
            return cost, path

        # Expand neighbors
        for neighbor, edge_cost in map.neighbors(current).items():
            if neighbor not in visited:
                new_cost = cost + edge_cost
                heapq.heappush(heap, (new_cost, neighbor, path + [neighbor]))

    # No path found
    return float('inf'), []