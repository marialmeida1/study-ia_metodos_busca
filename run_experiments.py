# run_experiments.py
# Executa experimentos com A* usando diferentes heurísticas e gera CSV com resultados.
import csv
from typing import List, Dict, Any
from astar import astar
from heuristics import HEURISTICS

def run_experiment(grid: List[List[int]], 
                   start: tuple, 
                   goal: tuple,
                   allow_diagonal: bool = False) -> List[Dict[str, Any]]:
    """
    Executa A* com todas as heurísticas disponíveis em um grid.
    
    Args:
        grid: matriz 2D (0=livre, 1=parede)
        start, goal: posições inicial e final
        allow_diagonal: permite movimentos diagonais
    
    Returns:
        lista de dicionários com resultados para cada heurística
    """
    results = []
    
    for heur_name, heur_func in HEURISTICS.items():
        result = astar(grid, start, goal, heur_func, allow_diagonal)
        
        results.append({
            'heuristic': heur_name,
            'path_found': result['path'] is not None,
            'time_s': result['metrics']['time_s'],
            'nodes_expanded': result['metrics']['nodes_expanded'],
            'nodes_generated': result['metrics']['nodes_generated'],
            'max_frontier_size': result['metrics']['max_frontier_size'],
            'path_cost': result['metrics']['path_cost'],
            'path_length': result['metrics']['path_length']
        })
    
    return results

def save_results_to_csv(results: List[Dict[str, Any]], filename: str = 'astar_results.csv'):
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
    
    print("\n" + "="*100)
    print(f"{'Heurística':<12} {'Tempo (s)':<12} {'Nós Exp.':<12} {'Nós Ger.':<12} "
          f"{'Front. Max':<12} {'Custo':<10} {'Tamanho':<10}")
    print("="*100)
    
    for r in results:
        print(f"{r['heuristic']:<12} "
              f"{r['time_s']:<12.6f} "
              f"{r['nodes_expanded']:<12} "
              f"{r['nodes_generated']:<12} "
              f"{r['max_frontier_size']:<12} "
              f"{str(r['path_cost']):<10} "
              f"{str(r['path_length']):<10}")
    
    print("="*100 + "\n")

# Exemplo de uso
if __name__ == '__main__':
    # Grid simples de exemplo (5x5)
    example_grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    
    start_pos = (0, 0)
    goal_pos = (4, 4)
    
    print("Executando experimentos com A*...")
    print(f"Grid: {len(example_grid)}x{len(example_grid[0])}")
    print(f"Início: {start_pos}, Meta: {goal_pos}\n")
    
    # Experimento sem diagonais
    results = run_experiment(example_grid, start_pos, goal_pos, allow_diagonal=False)
    print_results_table(results)
    save_results_to_csv(results, 'astar_results_4dir.csv')
    
    # Experimento com diagonais
    results_diag = run_experiment(example_grid, start_pos, goal_pos, allow_diagonal=True)
    print_results_table(results_diag)
    save_results_to_csv(results_diag, 'astar_results_8dir.csv')
