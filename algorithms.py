import heapq
from map import Map

def uniform_cost_search(map: Map, start: str, goal: str, heuristic=None, depth=None):
    """
    Finds the lowest-cost path between two cities using Uniform Cost Search.

    Parameters:
        map   (Map): Your Map instance with edges already populated
        start (str): Name of the starting city
        goal  (str): Name of the destination city

    Returns:
        A tuple (cost, path) where:
            status (str)      : "found" or "failure"
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
            return "found", cost, path

        # Expand neighbors
        for neighbor, edge_cost in map.neighbors(current).items():
            if neighbor not in visited:
                new_cost = cost + edge_cost
                heapq.heappush(heap, (new_cost, neighbor, path + [neighbor]))

    # No path found
    return "failure", float('inf'), []



def depth_limited_search(map: Map, start: str, goal: str, heuristic=None, depth: int = 10):
    """
    Finds a path between two cities using Depth-Limited Search.

    Parameters:
        map   (Map): Your Map instance with edges already populated
        start (str): Name of the starting city
        goal  (str): Name of the destination city
        limit (int): Maximum depth to explore

    Returns:
        A tuple (status, cost, path) where:
            status (str)          : "found", "cutoff", or "failure"
            cost   (int | float)  : Total distance if found, inf otherwise
            path   (list[str])    : Ordered list of cities, empty if not found
    """

    def recursive_dls(current, goal, limit, path, cost, visited):
        # Goal check
        if current == goal:
            return "found", cost, path

        # Depth limit reached — signal cutoff (goal might exist deeper)
        if limit == 0:
            return "cutoff", float("inf"), []

        cutoff_occurred = False
        visited.add(current)

        for neighbor, edge_cost in map.neighbors(current).items():
            if neighbor not in visited:
                result, total_cost, total_path = recursive_dls(
                    neighbor,
                    goal,
                    limit - 1,          # decrease remaining depth
                    path + [neighbor],
                    cost + edge_cost,
                    visited.copy()      # copy so sibling branches don't interfere
                )

                if result == "found":
                    return "found", total_cost, total_path
                elif result == "cutoff":
                    cutoff_occurred = True  # remember a cutoff happened

        # Distinguish between cutoff (maybe deeper) and full failure
        return ("cutoff" if cutoff_occurred else "failure"), float("inf"), []

    return recursive_dls(start, goal, depth, [start], 0, set())



def astar_search(map: Map, start: str, goal: str, heuristic: dict, depth=None):
    """
    Finds the lowest-cost path between two cities using A* Search.

    Parameters:
        map        (Map) : Your Map instance with edges already populated
        start      (str) : Name of the starting city
        goal       (str) : Name of the destination city
        heuristic  (dict): Estimated cost from each city to the goal
                           e.g. {"Lisboa": 245, "Porto": 497, "Faro": 0, ...}

    Returns:
        A tuple (cost, path) where:
            status (str)      : "found" or "failure"
            cost (int | float): Total distance of the optimal path
            path (list[str])  : Ordered list of cities from start to goal
        Returns (inf, []) if no path exists.
    """

    def h(city):
        """ Heuristic lookup — defaults to 0 if city not in dictionary. """
        return heuristic.get(city, 0)

    # Priority queue entries: (f = g + h, g = real cost, current_city, path)
    heap = [(0 + h(start), 0, start, [start])]

    # Best known g(n) for each city — only update if we find a cheaper route
    best_g = {start: 0}

    while heap:
        # f is unpacked as _ because it only serves as the heap's sorting key —
        # once the node is popped, the priority is irrelevant and only the real
        # cost g is used for all further calculations.
        _, g, current, path = heapq.heappop(heap)

        # If we popped an outdated entry, skip it
        if g > best_g.get(current, float("inf")):
            continue

        if current == goal:
            return "found", g, path

        for neighbor, edge_cost in map.neighbors(current).items():
            new_g = g + edge_cost
            if new_g < best_g.get(neighbor, float("inf")):
                best_g[neighbor] = new_g
                new_f = new_g + h(neighbor)
                heapq.heappush(heap, (new_f, new_g, neighbor, path + [neighbor]))

    return "failure", float("inf"), []



def greedy_best_first_search(map: Map, start: str, goal: str, heuristic: dict, depth=None):
    """
    Finds a path between two cities using Greedy Best-First Search
    (Procura Sôfrega).

    Unlike A*, this algorithm only uses the heuristic h(n) to prioritize
    nodes — it completely ignores the real accumulated cost g(n).
    This makes it faster in practice but NOT guaranteed to find the
    optimal (cheapest) path; it simply chases whatever looks closest
    to the goal according to the heuristic.

    f(n) = h(n)           # Greedy — only the heuristic matters
    f(n) = g(n) + h(n)    # A*     — balances real cost + heuristic

    Parameters:
        map        (Map) : Your Map instance with edges already populated
        start      (str) : Name of the starting city
        goal       (str) : Name of the destination city
        heuristic  (dict): Estimated cost from each city to the goal
                           e.g. {"Lisboa": 245, "Porto": 497, "Faro": 0, ...}

    Returns:
        A tuple (cost, path) where:
            status (str)      : "found" or "failure"
            cost (int | float): Total distance of the path found (not necessarily optimal)
            path (list[str])  : Ordered list of cities from start to goal
        Returns (inf, []) if no path exists.
    """

    def h(city):
        """
        Heuristic function h(n).
        This is the ONLY thing that drives priority in procura sôfrega —
        the real cost g(n) plays no role in node selection whatsoever.
        """
        return heuristic.get(city, 0)

    # Heap entries: (h(n), real cost so far, current city, path)
    # Note: unlike A*, we sort purely by h(n), not by g+h.
    # We still track the real cost so we can report it at the end,
    # but it never influences which node gets expanded next.
    heap = [(h(start), 0, start, [start])]

    # Visited set — since we don't track best_g, we just make sure
    # we never expand the same city twice (simple cycle prevention)
    visited = set()

    while heap:
        # h is unpacked as _ because once popped it serves no further purpose —
        # it was only used as the heap's sorting key to pick the most
        # promising node. The real cost g is what we carry forward.
        _, g, current, path = heapq.heappop(heap)

        if current in visited:
            continue
        visited.add(current)

        # Goal check — same as standard A*, we check on pop not on push
        if current == goal:
            return "found", g, path

        for neighbor, edge_cost in map.neighbors(current).items():
            if neighbor not in visited:
                heapq.heappush(heap, (
                    h(neighbor),        # priority is ONLY the heuristic
                    g + edge_cost,      # real cost tracked but not used for priority
                    neighbor,
                    path + [neighbor]
                ))

    return "failure", float("inf"), []