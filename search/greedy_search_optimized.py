# greedy_search_optimized.py
"""
Busca Gulosa (Greedy Best-First Search)

Características:
- Expande sempre o nó com menor valor heurístico h(n)
- Usa apenas a função heurística (não considera o custo do caminho)
- Não garante solução ótima
- É rápida e eficiente em termos de memória
- Completa em espaços finitos com detecção de estados repetidos
"""

import heapq
import time
from typing import Callable, List, Tuple, Union

from utils.search import SearchResult, get_neighbors

Position = Tuple[int, int]
Cell = Union[str, int]


def greedy_search(
    maze: List[List[Cell]],
    start: Position,
    goal: Position,
    heuristic: Callable[[Position, Position], float]
) -> SearchResult:
    """
    Busca Gulosa (Greedy Best-First Search).
    Expande sempre o nó com menor valor heurístico.
    
    Args:
        maze: matriz 2D onde 0/'S'/'G'=livre, 1=parede
        start: posição inicial (linha, coluna)
        goal: posição objetivo (linha, coluna)
        heuristic: função h(pos, goal) -> float
    
    Returns:
        SearchResult com caminho, profundidade, nós visitados e tempo
    """
    t0 = time.perf_counter()
    
    # Heap: (h, contador, posição, caminho)
    h_start = heuristic(start, goal)
    frontier = [(h_start, 0, start, [start])]
    visited = {start}
    counter = 1
    nodes_visited = 0
    max_frontier = 1
    
    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        h_current, _, current, path = heapq.heappop(frontier)
        nodes_visited += 1
        
        # Chegou ao objetivo
        if current == goal:
            t1 = time.perf_counter()
            path_cost = float(len(path) - 1)  # Custo = número de movimentos
            return SearchResult(
                found=True,
                path=path,
                depth=len(path) - 1,
                nodes_visited=nodes_visited,
                time=t1 - t0,
                nodes_generated=counter,
                max_frontier_size=max_frontier,
                path_cost=path_cost
            )
        
        # Expande vizinhos
        for neighbor in get_neighbors(current, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                h_neighbor = heuristic(neighbor, goal)
                new_path = path + [neighbor]
                heapq.heappush(frontier, (h_neighbor, counter, neighbor, new_path))
                counter += 1
    
    # Sem solução
    t1 = time.perf_counter()
    return SearchResult(
        found=False,
        path=[],
        depth=None,
        nodes_visited=nodes_visited,
        time=t1 - t0,
        nodes_generated=counter,
        max_frontier_size=max_frontier,
        path_cost=None
    )

