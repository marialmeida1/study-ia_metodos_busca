from collections import deque
import time
from typing import List, Tuple, Union

from utils.search import SearchResult, get_neighbors, reconstruct_path

Position = Tuple[int, int]
Cell = Union[str, int]


def bfs(maze: List[List[Cell]], start: Position, goal: Position) -> SearchResult:
    queue = deque([start])
    visited = set([start])
    parent: dict[Position, Position] = {}
    nodes_visited = 0

    t0 = time.time()

    while queue:
        current = queue.popleft()
        nodes_visited += 1

        if current == goal:
            t1 = time.time()
            path = reconstruct_path(parent, start, goal)
            depth = len(path) - 1
            return SearchResult(
                found=True,
                path=path,
                depth=depth,
                nodes_visited=nodes_visited,
                time=t1 - t0,
            )

        for neighbor in get_neighbors(current, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    t1 = time.time()
    return SearchResult(
        found=False,
        path=[],
        depth=None,
        nodes_visited=nodes_visited,
        time=t1 - t0,
    )
