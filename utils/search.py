from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Set, Union

Position = Tuple[int, int]
Cell = Union[str, int]

@dataclass
class SearchResult:
    found: bool
    path: List[Position]
    depth: int | None
    nodes_visited: int
    time: float


def get_neighbors(pos: Position, maze: List[List[Cell]]) -> List[Position]:
    """
    Retorna os vizinhos (cima, baixo, esquerda, direita) que:
    - Estão dentro dos limites da matriz
    - Não são obstáculos (valor 1)
    """
    rows = len(maze)
    cols = len(maze[0])
    r, c = pos

    candidates = [
        (r - 1, c),  
        (r + 1, c),  
        (r, c - 1),  
        (r, c + 1),  
    ]

    neighbors: List[Position] = []
    for nr, nc in candidates:
        if 0 <= nr < rows and 0 <= nc < cols:
            if maze[nr][nc] != 1: 
                neighbors.append((nr, nc))

    return neighbors


def reconstruct_path(
    parent: Dict[Position, Position],
    start: Position,
    goal: Position,
) -> List[Position]:
    """Reconstrói o caminho do objetivo até a origem usando o dicionário de pais."""
    path: List[Position] = []
    current = goal

    while current != start:
        path.append(current)
        current = parent[current]

    path.append(start)
    path.reverse()
    return path
