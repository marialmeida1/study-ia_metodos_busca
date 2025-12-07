# run_experiments.py
# Executa experimentos comparativos com DFS, BFS e A* (com 3 heurísticas) nos labirintos.
import csv
from typing import List, Dict, Any
from maze import MAZES, MAZE_DESCRIPTIONS, get_start_and_goal
from search.dfs import dfs
from search.bfs import bfs
from search.astar import astar
from search.heuristics import HEURISTICS


def run_experiment_on_maze(maze_id: int, allow_diagonal: bool = False) -> List[Dict[str, Any]]:
    """
    Executa DFS, BFS e A* (com 3 heurísticas) em um labirinto específico.
    
    Args:
        maze_id: ID do labirinto (1-9)
        allow_diagonal: permite movimentos diagonais
    
    Returns:
        lista de dicionários com resultados de cada algoritmo
    """
    maze = MAZES[maze_id]
    start, goal = get_start_and_goal(maze)
    results = []
    
    # DFS
    result_dfs = dfs(maze, start, goal)
    results.append({
        'maze_id': maze_id,
        'algorithm': 'DFS',
        'heuristic': '-',
        'path_found': result_dfs.found,
        'time_s': result_dfs.time,
        'nodes_visited': result_dfs.nodes_visited,
        'nodes_generated': '-',
        'max_frontier_size': '-',
        'path_cost': '-',
        'path_length': result_dfs.depth if result_dfs.found else None
    })
    
    # BFS
    result_bfs = bfs(maze, start, goal)
    results.append({
        'maze_id': maze_id,
        'algorithm': 'BFS',
        'heuristic': '-',
        'path_found': result_bfs.found,
        'time_s': result_bfs.time,
        'nodes_visited': result_bfs.nodes_visited,
        'nodes_generated': '-',
        'max_frontier_size': '-',
        'path_cost': '-',
        'path_length': result_bfs.depth if result_bfs.found else None
    })
    
    # A* com cada heurística
    for heur_name, heur_func in HEURISTICS.items():
        result_astar = astar(maze, start, goal, heur_func, allow_diagonal)
        results.append({
            'maze_id': maze_id,
            'algorithm': 'A*',
            'heuristic': heur_name,
            'path_found': result_astar.found,
            'time_s': result_astar.time,
            'nodes_visited': result_astar.nodes_visited,
            'nodes_generated': result_astar.nodes_generated,
            'max_frontier_size': result_astar.max_frontier_size,
            'path_cost': result_astar.path_cost,
            'path_length': result_astar.depth if result_astar.found else None
        })
    
    return results


def save_results_to_csv(results: List[Dict[str, Any]], filename: str = 'results/astar_results.csv'):
    """
    Salva resultados dos experimentos em arquivo CSV.
    
    Args:
        results: lista de dicionários com métricas
        filename: nome do arquivo CSV de saída
    """
    if not results:
        print("Nenhum resultado para salvar.")
        return
    
    fieldnames = results[0].keys()
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Resultados salvos em '{filename}'")

def print_results_table(results: List[Dict[str, Any]]):
    """Imprime resultados em formato de tabela legível."""
    if not results:
        print("Nenhum resultado para exibir.")
        return
    
    print("\n" + "="*120)
    print(f"{'Algoritmo':<10} {'Heurística':<12} {'Tempo (s)':<12} {'Nós Visit.':<12} "
          f"{'Nós Ger.':<12} {'Front. Max':<12} {'Custo':<10} {'Caminho':<10}")
    print("="*120)
    
    for r in results:
        print(f"{r['algorithm']:<10} "
              f"{str(r['heuristic']):<12} "
              f"{r['time_s']:<12.6f} "
              f"{r['nodes_visited']:<12} "
              f"{str(r['nodes_generated']):<12} "
              f"{str(r['max_frontier_size']):<12} "
              f"{str(r['path_cost']):<10} "
              f"{str(r['path_length']):<10}")
    
    print("="*120 + "\n")


def run_all_experiments(allow_diagonal: bool = False) -> List[Dict[str, Any]]:
    """
    Executa experimentos em todos os labirintos.
    
    Args:
        allow_diagonal: permite movimentos diagonais
    
    Returns:
        lista com todos os resultados consolidados
    """
    all_results = []
    
    for maze_id in MAZES.keys():
        print(f"Executando experimentos no Labirinto {maze_id}...")
        results = run_experiment_on_maze(maze_id, allow_diagonal)
        all_results.extend(results)
    
    return all_results


if __name__ == '__main__':
    print("="*120)
    print("EXPERIMENTOS COMPARATIVOS: DFS, BFS e A* (Manhattan, Euclidean, Chebyshev)")
    print("="*120)
    
    # Executa em todos os labirintos
    print("\n>>> Experimentos com movimentos em 4 direções (sem diagonais)\n")
    all_results = run_all_experiments(allow_diagonal=False)
    
    # Salva CSV consolidado
    save_results_to_csv(all_results, 'results/all_algorithms_comparison.csv')
    
    # Mostra estatísticas por labirinto
    for maze_id in MAZES.keys():
        maze_results = [r for r in all_results if r['maze_id'] == maze_id]
        print(f"\n{'='*120}")
        print(f"LABIRINTO {maze_id}: {MAZE_DESCRIPTIONS[maze_id]}")
        print(f"{'='*120}")
        print_results_table(maze_results)
    
    print("\n✅ Experimentos concluídos! Resultados salvos em 'results/all_algorithms_comparison.csv'")
