"""
Características da Busca Gulosa:
- Expande sempre o nó com menor valor heurístico h(n)
- Usa apenas a função heurística (não considera o custo do caminho)
- Não garante solução ótima
- É rápida e eficiente em termos de memória
- Completa em espaços finitos com detecção de estados repetidos
"""

import heapq
import time
from typing import Callable, List, Set, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class SearchResult:
    found: bool = False
    path: List[Tuple[int, int]] = field(default_factory=list)
    nodes_visited: int = 0
    solution_depth: int = 0
    execution_time: float = 0.0
    visited_nodes: Set[Tuple[int, int]] = field(default_factory=set)
    max_frontier_size: int = 0  


class GreedySearch:

    def __init__(self, maze):
        self.maze = maze
    
    def search(self, heuristic: Callable[[Tuple[int, int]], float]) -> SearchResult:

        result = SearchResult()
        start_time = time.perf_counter()
        
        start_pos = self.maze.start
        h_start = heuristic(start_pos)
        
        frontier = [(h_start, 0, start_pos, [start_pos])]
        visited = {start_pos}
        
        counter = 1
        result.nodes_visited = 1
        
        while frontier:
            result.max_frontier_size = max(result.max_frontier_size, len(frontier))
            
            h_current, _, current_pos, path = heapq.heappop(frontier)
            
            if self.maze.is_goal(current_pos):
                result.found = True
                result.path = path
                result.solution_depth = len(path) - 1
                result.execution_time = time.perf_counter() - start_time
                result.visited_nodes = visited
                return result
            
            for neighbor in self.maze.get_neighbors(current_pos):
                if neighbor not in visited:
                    visited.add(neighbor)
                    result.nodes_visited += 1
                    
                    h_neighbor = heuristic(neighbor)
                    new_path = path + [neighbor]
                    
                    heapq.heappush(frontier, (h_neighbor, counter, neighbor, new_path))
                    counter += 1
        
        result.found = False
        result.execution_time = time.perf_counter() - start_time
        result.visited_nodes = visited
        return result

# FUNÇÕES GENÉRICAS DE CUSTO

def uniform_cost(from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> float:
    return 1.0


def euclidean_cost(from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> float:
    return ((to_pos[0] - from_pos[0]) ** 2 + (to_pos[1] - from_pos[1]) ** 2) ** 0.5


def manhattan_cost(from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> float:
    return abs(to_pos[0] - from_pos[0]) + abs(to_pos[1] - from_pos[1])


def weighted_cost(from_pos: Tuple[int, int], to_pos: Tuple[int, int], 
                  weight_map: dict = None) -> float:
    if weight_map is None:
        return 1.0
    return weight_map.get(to_pos, 1.0)


def create_cost_function(cost_type: str = "uniform", weight_map: dict = None):
    cost_functions = {
        "uniform": uniform_cost,
        "euclidean": euclidean_cost,
        "manhattan": manhattan_cost,
        "weighted": lambda f, t: weighted_cost(f, t, weight_map)
    }
    
    if cost_type not in cost_functions:
        raise ValueError(f"Tipo de custo inválido: {cost_type}. "
                        f"Opções: {list(cost_functions.keys())}")
    
    return cost_functions[cost_type]

# FUNÇÕES GENÉRICAS DE HEURÍSTICA

def manhattan_heuristic(pos: Tuple[int, int], goal: Tuple[int, int]) -> float:
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])


def euclidean_heuristic(pos: Tuple[int, int], goal: Tuple[int, int]) -> float:
    return ((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2) ** 0.5


def chebyshev_heuristic(pos: Tuple[int, int], goal: Tuple[int, int]) -> float:
    return max(abs(pos[0] - goal[0]), abs(pos[1] - goal[1]))


def octile_heuristic(pos: Tuple[int, int], goal: Tuple[int, int], 
                     D: float = 1.0, D2: float = 1.414) -> float:
    dx = abs(pos[0] - goal[0])
    dy = abs(pos[1] - goal[1])
    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)


def zero_heuristic(pos: Tuple[int, int], goal: Tuple[int, int]) -> float:
    return 0.0


def custom_weighted_heuristic(pos: Tuple[int, int], goal: Tuple[int, int], 
                               weight: float = 1.0, base_heuristic = None) -> float:
    if base_heuristic is None:
        base_heuristic = euclidean_heuristic
    return weight * base_heuristic(pos, goal)


def create_heuristic_function(heuristic_type: str = "manhattan", 
                               goal: Tuple[int, int] = None,
                               **kwargs):
    if goal is None:
        raise ValueError("É necessário fornecer a posição objetivo (goal)")
    
    heuristic_map = {
        "manhattan": lambda pos: manhattan_heuristic(pos, goal),
        "euclidean": lambda pos: euclidean_heuristic(pos, goal),
        "chebyshev": lambda pos: chebyshev_heuristic(pos, goal),
        "octile": lambda pos: octile_heuristic(pos, goal, 
                                               kwargs.get('D', 1.0), 
                                               kwargs.get('D2', 1.414)),
        "zero": lambda pos: zero_heuristic(pos, goal),
        "weighted": lambda pos: custom_weighted_heuristic(
            pos, goal, 
            kwargs.get('weight', 1.0),
            kwargs.get('base_heuristic', euclidean_heuristic)
        )
    }
    
    if heuristic_type not in heuristic_map:
        raise ValueError(f"Tipo de heurística inválido: {heuristic_type}. "
                        f"Opções: {list(heuristic_map.keys())}")
    
    return heuristic_map[heuristic_type]

""""
# EXEMPLO DE TESTE

if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DE BUSCA GULOSA")
    print("=" * 60)
    
    class SimpleMaze:
        def __init__(self, width, height, start, goal, obstacles=None):
            self.width = width
            self.height = height
            self.start = start
            self.goal = goal
            self.obstacles = obstacles or set()
        
        def is_goal(self, pos):
            return pos == self.goal
        
        def get_neighbors(self, pos):
            x, y = pos
            neighbors = []
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width and 
                    0 <= ny < self.height and 
                    (nx, ny) not in self.obstacles):
                    neighbors.append((nx, ny))
            return neighbors
    
    print("\n--- TESTE 1: Grid 5x5 sem obstáculos ---")
    maze1 = SimpleMaze(5, 5, (0, 0), (4, 4))
    
    h_manhattan = create_heuristic_function("manhattan", goal=maze1.goal)
    
    searcher = GreedySearch(maze1)
    result = searcher.search(h_manhattan)
    
    print(f"Solução encontrada: {result.found}")
    if result.found:
        print(f"Caminho: {result.path}")
        print(f"Profundidade: {result.solution_depth}")
    print(f"Nós visitados: {result.nodes_visited}")
    print(f"Tempo: {result.execution_time:.6f}s")
    print(f"Max frontier: {result.max_frontier_size}")
    
    print("\n--- TESTE 2: Grid 6x6 com obstáculos ---")
    obstacles = {(2, 0), (2, 1), (2, 2), (2, 3)}  
    maze2 = SimpleMaze(6, 6, (0, 0), (5, 5), obstacles)
    
    heuristics = {
        "Manhattan": create_heuristic_function("manhattan", goal=maze2.goal),
        "Euclidean": create_heuristic_function("euclidean", goal=maze2.goal),
        "Chebyshev": create_heuristic_function("chebyshev", goal=maze2.goal)
    }
    
    for h_name, h_func in heuristics.items():
        searcher = GreedySearch(maze2)
        result = searcher.search(h_func)
        print(f"\n{h_name}:")
        print(f"  Solução: {result.found}")
        if result.found:
            print(f"  Profundidade: {result.solution_depth}")
        print(f"  Nós visitados: {result.nodes_visited}")
        print(f"  Tempo: {result.execution_time:.6f}s")
    
    print("\n--- TESTE 3: Funções de custo ---")
    cost_uniform = create_cost_function("uniform")
    cost_manhattan = create_cost_function("manhattan")
    cost_euclidean = create_cost_function("euclidean")
    
    from_pos = (0, 0)
    to_pos = (3, 4)
    
    print(f"Custo de {from_pos} para {to_pos}:")
    print(f"  Uniforme: {cost_uniform(from_pos, to_pos):.2f}")
    print(f"  Manhattan: {cost_manhattan(from_pos, to_pos):.2f}")
    print(f"  Euclidiana: {cost_euclidean(from_pos, to_pos):.2f}")
    
    print("\n--- TESTE 4: Comparação de heurísticas ---")
    pos = (2, 3)
    goal = (8, 7)
    
    print(f"Heurísticas de {pos} para {goal}:")
    print(f"  Manhattan: {manhattan_heuristic(pos, goal):.2f}")
    print(f"  Euclidean: {euclidean_heuristic(pos, goal):.2f}")
    print(f"  Chebyshev: {chebyshev_heuristic(pos, goal):.2f}")
    print(f"  Octile: {octile_heuristic(pos, goal):.2f}")
    print(f"  Zero: {zero_heuristic(pos, goal):.2f}")
    
    print("\n--- TESTE 5: Heurística ponderada (Weighted) ---")
    h_weighted_1 = create_heuristic_function("weighted", goal=maze2.goal, weight=1.0)
    h_weighted_2 = create_heuristic_function("weighted", goal=maze2.goal, weight=2.0)
    
    searcher = GreedySearch(maze2)
    
    result1 = searcher.search(h_weighted_1)
    print(f"Weight=1.0: Nós={result1.nodes_visited}, Prof={result1.solution_depth if result1.found else 'N/A'}")
    
    result2 = searcher.search(h_weighted_2)
    print(f"Weight=2.0: Nós={result2.nodes_visited}, Prof={result2.solution_depth if result2.found else 'N/A'}")
    
    print("\n" + "=" * 60)
    print("TESTES CONCLUÍDOS!")
    print("=" * 60)
""""