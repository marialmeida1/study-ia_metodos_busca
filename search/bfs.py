# bfs.py
# BFS (Breadth-First Search) - busca em largura usando fila.
from collections import deque
import time
from typing import List, Tuple, Union

from utils.search import SearchResult, get_neighbors, reconstruct_path

Position = Tuple[int, int]
Cell = Union[str, int]


def bfs(maze: List[List[Cell]], start: Position, goal: Position) -> SearchResult:
    """Busca em largura. Explora nível por nível, garante caminho mais curto."""
    queue = deque([start])  # Fila FIFO para processar nós
    visited = set([start])  # Marca nós já visitados
    parent: dict[Position, Position] = {}  # Rastreia caminho
    nodes_visited = 0

    t0 = time.time()

    while queue:
        current = queue.popleft()  # Remove do início da fila
        nodes_visited += 1

        if current == goal:  # Encontrou o objetivo
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

        # Explora vizinhos não visitados
        for neighbor in get_neighbors(current, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)  # Adiciona no fim da fila

    t1 = time.time()
    return SearchResult(
        found=False,
        path=[],
        depth=None,
        nodes_visited=nodes_visited,
        time=t1 - t0,
    )
