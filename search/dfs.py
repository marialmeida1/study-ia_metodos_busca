# dfs.py
# DFS (Depth-First Search) - busca em profundidade usando pilha.
import time
from typing import List, Tuple, Union

from utils.search import SearchResult, get_neighbors, reconstruct_path

Position = Tuple[int, int]
Cell = Union[str, int]


def dfs(maze: List[List[Cell]], start: Position, goal: Position) -> SearchResult:
    """Busca em profundidade. Explora o mais fundo possível antes de retroceder."""
    stack = [start]  # Pilha LIFO para processar nós
    visited = set([start])  # Marca nós já visitados
    parent: dict[Position, Position] = {}  # Rastreia caminho
    nodes_visited = 0

    t0 = time.time()

    while stack:
        current = stack.pop()  # Remove do topo da pilha
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
                stack.append(neighbor)  # Adiciona no topo da pilha

    t1 = time.time()
    return SearchResult(
        found=False,
        path=[],
        depth=None,
        nodes_visited=nodes_visited,
        time=t1 - t0,
    )
