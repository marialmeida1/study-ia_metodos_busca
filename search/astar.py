# astar.py
# Implementação do A* (f = g + h) para labirintos.
import heapq
import time
from typing import Callable, Dict, List, Tuple, Optional, Set, Union

from utils.search import SearchResult

Pos = Tuple[int,int]
Cell = Union[str, int]

class Node:
    """Nó da árvore de busca com posição, custo g, f e referência ao pai."""
    def __init__(self, pos: Pos, g: float, f: float, parent: Optional['Node']):
        self.pos = pos
        self.g = g      # custo do caminho até aqui
        self.f = f      # f = g + h (estimativa total)
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f

def reconstruct_path(node: Node) -> List[Pos]:
    """Reconstrói o caminho do início até o nó final."""
    path = []
    cur = node
    while cur:
        path.append(cur.pos)
        cur = cur.parent
    path.reverse()
    return path

def neighbors_4(pos: Pos):
    """Retorna vizinhos nas 4 direções (cima, baixo, esquerda, direita)."""
    x,y = pos
    return [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]

def neighbors_8(pos: Pos):
    """Retorna vizinhos nas 8 direções (incluindo diagonais)."""
    x,y = pos
    return [(x+1,y),(x-1,y),(x,y+1),(x,y-1),
            (x+1,y+1),(x+1,y-1),(x-1,y+1),(x-1,y-1)]

def astar(maze: List[List[Cell]],
          start: Pos,
          goal: Pos,
          heuristic: Callable[[Pos,Pos], float],
          allow_diagonal: bool = False,
          diag_cost: float = 1.41421356237) -> SearchResult:
    """
    Algoritmo A* completo para busca em labirinto.
    
    Args:
        maze: matriz 2D onde 0/'S'/'G'=livre, 1=parede
        start, goal: posições (linha, coluna)
        heuristic: função h(pos, goal) -> float
        allow_diagonal: permite movimentos diagonais
        diag_cost: custo do movimento diagonal (padrão √2)
    
    Returns:
        SearchResult com caminho, profundidade, nós visitados, tempo e métricas adicionais
    """
    t0 = time.perf_counter()
    rows = len(maze)
    cols = len(maze[0]) if rows>0 else 0

    def is_walkable(pos: Pos) -> bool:
        """Verifica se a posição é válida e caminhável."""
        if not (0 <= pos[0] < rows and 0 <= pos[1] < cols):
            return False
        return maze[pos[0]][pos[1]] != 1
    
    neigh_func = neighbors_8 if allow_diagonal else neighbors_4

    open_heap: List[Tuple[float,int,Node]] = []
    entry_count = 0
    start_node = Node(start, 0.0, heuristic(start,goal), None)
    heapq.heappush(open_heap, (start_node.f, entry_count, start_node))
    entry_count += 1

    came_g: Dict[Pos,float] = {start: 0.0}
    closed: Set[Pos] = set()

    nodes_expanded = 0
    nodes_generated = 1
    max_frontier = 1

    while open_heap:
        max_frontier = max(max_frontier, len(open_heap))
        _, _, current = heapq.heappop(open_heap)

        # Ignora nós com g desatualizado (caminho melhor já encontrado).
        if came_g.get(current.pos, float('inf')) < current.g:
            continue

        nodes_expanded += 1

        if current.pos == goal:
            t1 = time.perf_counter()
            path = reconstruct_path(current)
            return SearchResult(
                found=True,
                path=path,
                depth=len(path) - 1,
                nodes_visited=nodes_expanded,
                time=t1 - t0,
                nodes_generated=nodes_generated,
                max_frontier_size=max_frontier,
                path_cost=current.g
            )

        closed.add(current.pos)

        for nb in neigh_func(current.pos):
            if not is_walkable(nb):
                continue

            # Custo do movimento: diagonal vs reto.
            step_cost = (diag_cost if (nb[0]!=current.pos[0] and nb[1]!=current.pos[1]) else 1.0)
            tentative_g = current.g + step_cost

            if nb in closed and tentative_g >= came_g.get(nb, float('inf')):
                continue

            if tentative_g < came_g.get(nb, float('inf')):
                came_g[nb] = tentative_g
                f = tentative_g + heuristic(nb, goal)
                child = Node(nb, tentative_g, f, current)
                heapq.heappush(open_heap, (f, entry_count, child))
                entry_count += 1
                nodes_generated += 1

    # Sem solução.
    t1 = time.perf_counter()
    return SearchResult(
        found=False,
        path=[],
        depth=None,
        nodes_visited=nodes_expanded,
        time=t1 - t0,
        nodes_generated=nodes_generated,
        max_frontier_size=max_frontier,
        path_cost=None
    )
