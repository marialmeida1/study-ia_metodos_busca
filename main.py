from pprint import pprint

from maze import MAZES, MAZE_DESCRIPTIONS, get_start_and_goal
from search.bfs import bfs
from search.dfs import dfs


def print_maze_with_path(maze, path):
    """Imprime o labirinto marcando o caminho com '*'."""
    path_set = set(path)
    for r, row in enumerate(maze):
        line = []
        for c, cell in enumerate(row):
            if (r, c) in path_set and cell not in ("S", "G"):
                line.append("*")
            else:
                line.append(str(cell))
        print(" ".join(line))
    print()

def show_menu():
    print("\n=== MENU DE LABIRINTOS ===")
    print("0 - Sair")
    for i in range(1, 10):
        desc = MAZE_DESCRIPTIONS[i]
        print(f"{i} - Labirinto {i}: {desc}")

def main():
    while True:
        show_menu()
        choice = input("Escolha uma opção: ").strip()

        # validação básica
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

        # pega o labirinto escolhido
        maze = MAZES[option]
        start, goal = get_start_and_goal(maze)

        print("\nLabirinto escolhido:")
        print_maze_with_path(maze, [])

        # ================== BFS ==================
        print("=== BFS ===")
        result_bfs = bfs(maze, start, goal)
        pprint(result_bfs.__dict__)
        if result_bfs.found:
            print("\nLabirinto com caminho (BFS):")
            print_maze_with_path(maze, result_bfs.path)

        # ================== DFS ==================
        print("=== DFS ===")
        result_dfs = dfs(maze, start, goal)
        pprint(result_dfs.__dict__)
        if result_dfs.found:
            print("\nLabirinto com caminho (DFS):")
            print_maze_with_path(maze, result_dfs.path)

        input("Pressione ENTER para voltar ao menu...")


if __name__ == "__main__":
    main()