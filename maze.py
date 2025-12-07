# maze.py
# Definição dos 9 labirintos usados nos experimentos.
from typing import List, Tuple, Union

Position = Tuple[int, int]  # (linha, coluna)
Cell = Union[str, int]  # Célula pode ser 'S', 'G', 0 (livre) ou 1 (parede)

MAZE_1: List[List[Cell]] = [
    ["S", 0,   0,   1,   0],
    [0,   1,   0,   1,   0],
    [0,   0,   0,   0,   0],
    [1,   1,   0,   1,  "G"],
]

MAZE_2: List[List[Cell]] = [
    ["S", 0, 1, 0, 0],
    [0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0],
    [1, 1, 1, 1, 0],
    [0, 0, 0, 0, "G"],
]

MAZE_3: List[List[Cell]] = [
    ["S", 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 1],
    [0, 0, 0, 0, 1, "G"]
]

MAZE_4: List[List[Cell]] = [
    ["S", 0, 1, 0, 0, 0, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [1, 0, 0, 0, 1, 1, 0],
    [1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, "G"]
]

MAZE_5: List[List[Cell]] = [
    ["S", 0, 0, 0, 0, 0, 0, 0, "G"]
]

MAZE_6: List[List[Cell]] = [
    ["S", 0, 0, 1, 0, 0],
    [1, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, "G"],
    [0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0],
]

MAZE_7: List[List[Cell]] = [
    ["S", 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, "G"],
    [1, 1, 1, 1, 1, 1, 1]
]

MAZE_8: List[List[Cell]] = [
    ["S", 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 1, 1, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, "G"]
]

MAZE_9: List[List[Cell]] = [
    ["S",0,1,0,0,0,1,0,0,0,0,1,0,0,0],
    [0,0,1,0,1,0,1,0,1,1,0,1,1,1,0],
    [1,0,0,0,1,0,0,0,0,1,0,0,0,1,0],
    [1,1,1,0,1,1,1,1,0,1,1,1,0,1,0],
    [0,0,0,0,0,1,0,0,0,0,0,1,0,0,"G"]
]

MAZES: dict[int, List[List[Cell]]] = {
    1: MAZE_1,
    2: MAZE_2,
    3: MAZE_3,
    4: MAZE_4,
    5: MAZE_5,
    6: MAZE_6,
    7: MAZE_7,
    8: MAZE_8,
    9: MAZE_9,
}

MAZE_DESCRIPTIONS = {
    1: "Pequeno e simples; caminho curto com poucos desvios.",
    2: "Pequeno com obstáculos moderados; alguns becos sem saída leves.",
    3: "Médio com múltiplas rotas possíveis e caminhos alternativos.",
    4: "Labirinto clássico com túneis e escolhas profundas.",
    5: "Linha reta; ideal para testar profundidade e performance mínima.",
    6: "Vários becos sem saída; ótimo para testar DFS vs BFS.",
    7: "Corredor longo e estreito; DFS tende a performar muito bem.",
    8: "Alta densidade de obstáculos; excelente para ver A* brilhar.",
    9: "Grande e complexo; ideal para comparar algoritmos em larga escala.",
}

def find_symbol(maze: List[List[Cell]], symbol: str) -> Position:
    """Encontra a posição (linha, coluna) de um símbolo no labirinto."""
    for r, row in enumerate(maze):
        for c, value in enumerate(row):
            if value == symbol:
                return (r, c)
    raise ValueError(f"Símbolo {symbol!r} não encontrado no labirinto.")


def get_start_and_goal(maze: List[List[Cell]]) -> tuple[Position, Position]:
    """Retorna a posição inicial (S) e final (G)."""
    start = find_symbol(maze, "S")
    goal = find_symbol(maze, "G")
    return start, goal
