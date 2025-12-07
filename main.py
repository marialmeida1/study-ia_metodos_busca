# main.py
# Interface interativa para testar DFS, BFS e A* nos labirintos.
from pprint import pprint

from maze import MAZES, MAZE_DESCRIPTIONS, get_start_and_goal
from search.bfs import bfs
from search.dfs import dfs
from search.astar import astar
from search.heuristics import HEURISTICS


def print_maze_with_path(maze, path):
    """Imprime o labirinto marcando o caminho com '*'."""
    path_set = set(path)  # Para busca rápida
    for r, row in enumerate(maze):
        line = []
        for c, cell in enumerate(row):
            # Marca caminho com * (exceto S e G)
            if (r, c) in path_set and cell not in ("S", "G"):
                line.append("*")
            else:
                line.append(str(cell))
        print(" ".join(line))
    print()

def show_menu():
    """Exibe menu com os 9 labirintos disponíveis."""
    print("\n=== MENU DE LABIRINTOS ===")
    print("0 - Sair")
    for i in range(1, 10):
        desc = MAZE_DESCRIPTIONS[i]
        print(f"{i} - Labirinto {i}: {desc}")

def choose_heuristic():
    """Menu para escolher a heurística do A*."""
    print("\n=== ESCOLHA A HEURÍSTICA ===")
    heuristics_list = list(HEURISTICS.keys())
    for idx, name in enumerate(heuristics_list, 1):
        print(f"{idx} - {name.capitalize()}")
    
    while True:
        choice = input("Escolha a heurística (1-3): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(heuristics_list):
            return heuristics_list[int(choice) - 1]
        print("Opção inválida. Tente novamente.")

def main():
    """Loop principal do menu interativo."""
    while True:
        show_menu()
        choice = input("Escolha uma opção: ").strip()

        # Validação de entrada
        if not choice.isdigit():
            print("Por favor, digite um número válido.")
            continue

        option = int(choice)

        if option == 0:
            print("Encerrando o programa. Até mais!")
            break

        if option not in MAZES:
            print("Opção inválida. Tente novamente.")
            continue

        # Carrega labirinto escolhido
        maze = MAZES[option]
        start, goal = get_start_and_goal(maze)

        print("\nLabirinto escolhido:")
        print_maze_with_path(maze, [])

        # Escolhe o algoritmo
        print("\n=== ESCOLHA O ALGORITMO ===")
        print("1 - DFS (Depth-First Search)")
        print("2 - BFS (Breadth-First Search)")
        print("3 - A* (A-Star)")
        
        algo_choice = input("Escolha o algoritmo (1-3): ").strip()
        
        if algo_choice == '1':
            # ================== DFS ==================
            print("\n=== DFS ===")
            result = dfs(maze, start, goal)
            pprint(result.__dict__)
            if result.found:
                print("\nLabirinto com caminho (DFS):")
                print_maze_with_path(maze, result.path)
        
        elif algo_choice == '2':
            # ================== BFS ==================
            print("\n=== BFS ===")
            result = bfs(maze, start, goal)
            pprint(result.__dict__)
            if result.found:
                print("\nLabirinto com caminho (BFS):")
                print_maze_with_path(maze, result.path)
        
        elif algo_choice == '3':
            # ================== A* ==================
            heur_name = choose_heuristic()
            heur_func = HEURISTICS[heur_name]
            
            print(f"\n=== A* (Heurística: {heur_name.capitalize()}) ===")
            result = astar(maze, start, goal, heur_func, allow_diagonal=False)
            pprint(result.__dict__)
            if result.found:
                print(f"\nLabirinto com caminho (A* - {heur_name.capitalize()}):")
                print_maze_with_path(maze, result.path)
        
        else:
            print("Algoritmo inválido.")
        
        input("\nPressione ENTER para voltar ao menu...")

if __name__ == "__main__":
    main()