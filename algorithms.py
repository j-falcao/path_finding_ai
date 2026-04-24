import heapq
from map import Map


def uniform_cost_search(map: Map, start: str, goal: str, heuristic=None, depth=None):

    heap = [(0, start, [start])]
    visited = {}

    iterations = []
    iteration_num = 0

    while heap:
        cost, current, path = heapq.heappop(heap)

        if current in visited:
            continue

        visited[current] = cost

        iteration_num += 1
        iterations.append({
            "iteration": iteration_num,
            "expanded_node": current,
            "g_cost": cost,
            "frontier_size": len(heap),
            "path": path.copy()
        })

        if current == goal:
            return "found", cost, path, iterations

        for neighbor, edge_cost in map.neighbors(current).items():
            if neighbor not in visited:
                new_cost = cost + edge_cost
                heapq.heappush(
                    heap,
                    (new_cost, neighbor, path + [neighbor])
                )

    return "failure", float("inf"), [], iterations



def depth_limited_search(map: Map, start: str, goal: str, heuristic=None, depth=10):

    iterations = []
    iteration_num = [0]

    def recursive_dls(current, goal, limit, path, cost, visited):

        iteration_num[0] += 1

        iterations.append({
            "iteration": iteration_num[0],
            "expanded_node": current,
            "depth_remaining": limit,
            "g_cost": cost,
            "path": path.copy()
        })

        if current == goal:
            return "found", cost, path

        if limit == 0:
            return "cutoff", None, []

        cutoff_occurred = False
        visited.add(current)

        for neighbor, edge_cost in map.neighbors(current).items():
            if neighbor not in visited:

                result, total_cost, total_path = recursive_dls(
                    neighbor,
                    goal,
                    limit - 1,
                    path + [neighbor],
                    cost + edge_cost,
                    visited.copy()
                )

                if result == "found":
                    return "found", total_cost, total_path

                elif result == "cutoff":
                    cutoff_occurred = True

        return ("cutoff" if cutoff_occurred else "failure"), None, []

    result = recursive_dls(start, goal, depth, [start], 0, set())

    return result[0], result[1], result[2], iterations



def astar_search(map: Map, start: str, goal: str, heuristic: dict, depth=None):

    def h(city):
        return heuristic.get(city, 0)

    heap = [(h(start), 0, start, [start])]
    best_g = {start: 0}

    iterations = []
    iteration_num = 0

    while heap:

        f, g, current, path = heapq.heappop(heap)

        if g > best_g.get(current, float("inf")):
            continue

        iteration_num += 1

        iterations.append({
            "iteration": iteration_num,
            "expanded_node": current,
            "g_cost": g,
            "h_cost": h(current),
            "f_cost": f,
            "frontier_size": len(heap),
            "path": path.copy()
        })

        if current == goal:
            return "found", g, path, iterations

        for neighbor, edge_cost in map.neighbors(current).items():

            new_g = g + edge_cost

            if new_g < best_g.get(neighbor, float("inf")):

                best_g[neighbor] = new_g
                new_f = new_g + h(neighbor)

                heapq.heappush(
                    heap,
                    (new_f, new_g, neighbor, path + [neighbor])
                )

    return "failure", float("inf"), [], iterations



def greedy_best_first_search(map: Map, start: str, goal: str, heuristic: dict, depth=None):

    def h(city):
        return heuristic.get(city, 0)

    heap = [(h(start), 0, start, [start])]
    visited = set()

    iterations = []
    iteration_num = 0

    while heap:

        h_val, g, current, path = heapq.heappop(heap)

        if current in visited:
            continue

        visited.add(current)

        iteration_num += 1

        iterations.append({
            "iteration": iteration_num,
            "expanded_node": current,
            "g_cost": g,
            "h_cost": h_val,
            "frontier_size": len(heap),
            "path": path.copy()
        })

        if current == goal:
            return "found", g, path, iterations

        for neighbor, edge_cost in map.neighbors(current).items():

            if neighbor not in visited:

                heapq.heappush(
                    heap,
                    (
                        h(neighbor),
                        g + edge_cost,
                        neighbor,
                        path + [neighbor]
                    )
                )

    return "failure", float("inf"), [], iterations
