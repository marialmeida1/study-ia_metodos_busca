# heuristics.py
# Três heurísticas para grid: manhattan, euclidiana, chebyshev
import math
from typing import Tuple

Pos = Tuple[int,int]

def manhattan(a: Pos, b: Pos) -> float:
    """Distância Manhattan (L1). Boa para movimentos 4-direções."""
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def euclidean(a: Pos, b: Pos) -> float:
    """Distância Euclidiana (L2). Boa para movimentos em qualquer direção."""
    return math.hypot(a[0]-b[0], a[1]-b[1])

def chebyshev(a: Pos, b: Pos) -> float:
    """Distância Chebyshev (L∞). Útil quando movimentos diagonais custam 1."""
    return max(abs(a[0]-b[0]), abs(a[1]-b[1]))

# Interface: mapa de heurísticas disponíveis para seleção.
HEURISTICS = {
    'manhattan': manhattan,
    'euclidean': euclidean,
    'chebyshev': chebyshev
}
