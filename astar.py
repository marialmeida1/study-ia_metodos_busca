# astar.py
# Implementação do A* (f = g + h) para grid. Retorna caminho e métricas.
import heapq
import time
from typing import Callable, Dict, List, Tuple, Optional, Set

Pos = Tuple[int,int]

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

def astar(grid: List[List[int]],
          start: Pos,
          goal: Pos,
          heuristic: Callable[[Pos,Pos], float],
          allow_diagonal: bool = False,
          diag_cost: float = 1.41421356237) -> Dict:
    """
    Algoritmo A* completo para busca em grid.
    
    Args:
        grid: matriz 2D onde 0=livre, 1=parede
        start, goal: posições (linha, coluna)
        heuristic: função h(pos, goal) -> float
        allow_diagonal: permite movimentos diagonais
        diag_cost: custo do movimento diagonal (padrão √2)
    
    Returns:
        dict com 'path' (lista de posições ou None) e 'metrics' (tempo, nós expandidos,
        nós gerados, tamanho máximo da fronteira, custo do caminho, comprimento do caminho)
    """
    t0 = time.perf_counter()
    rows = len(grid)
    cols = len(grid[0]) if rows>0 else 0

    in_bounds = lambda p: 0 <= p[0] < rows and 0 <= p[1] < cols
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
            return {
                'path': path,
                'metrics': {
                    'time_s': t1 - t0,
                    'nodes_expanded': nodes_expanded,
                    'nodes_generated': nodes_generated,
                    'max_frontier_size': max_frontier,
                    'path_cost': current.g,
                    'path_length': len(path)-1  # number of moves
                }
            }

        closed.add(current.pos)

        for nb in neigh_func(current.pos):
            if not in_bounds(nb): 
                continue
            if grid[nb[0]][nb[1]] == 1:  # parede
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
    return {
        'path': None,
        'metrics': {
            'time_s': t1 - t0,
            'nodes_expanded': nodes_expanded,
            'nodes_generated': nodes_generated,
            'max_frontier_size': max_frontier,
            'path_cost': None,
            'path_length': None
        }
    }
