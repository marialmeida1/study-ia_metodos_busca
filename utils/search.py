# search.py
# Utilitários compartilhados por todos os algoritmos de busca.
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Set, Union, Optional

Position = Tuple[int, int]
Cell = Union[str, int]

@dataclass
class SearchResult:
    """Resultado padronizado de um algoritmo de busca."""
    found: bool  # Solução encontrada?
    path: List[Position]  # Caminho da origem ao objetivo
    depth: int | None  # Profundidade (número de movimentos)
    nodes_visited: int  # Nós expandidos
    time: float  # Tempo de execução
    # Campos extras para A*
    nodes_generated: Optional[int] = None  # Total de nós gerados
    max_frontier_size: Optional[int] = None  # Tamanho máximo da fronteira
    path_cost: Optional[float] = None # Custo total do caminho


def get_neighbors(pos: Position, maze: List[List[Cell]]) -> List[Position]:
    """
    Retorna os vizinhos (cima, baixo, esquerda, direita) que:
    - Estão dentro dos limites da matriz
    - Não são obstáculos (valor 1)
    """
    rows = len(maze)
    cols = len(maze[0])
    r, c = pos

    # Possíveis vizinhos: cima, baixo, esquerda, direita
    candidates = [
        (r - 1, c),  # Cima
        (r + 1, c),  # Baixo
        (r, c - 1),  # Esquerda
        (r, c + 1),  # Direita
    ]

    neighbors: List[Position] = []
    for nr, nc in candidates:
        # Verifica limites e se não é parede (1)
        if 0 <= nr < rows and 0 <= nc < cols:
            if maze[nr][nc] != 1: 
                neighbors.append((nr, nc))
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
