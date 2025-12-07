# Projeto: Métodos de Busca em Labirintos

Implementação e comparação de algoritmos de busca (DFS, BFS e A*) aplicados a labirintos.

## 📁 Estrutura do Projeto

```
study-ia_metodos_busca/
├── search/                    # Algoritmos de busca
│   ├── __init__.py
│   ├── dfs.py                # Depth-First Search
│   ├── bfs.py                # Breadth-First Search
│   ├── astar.py              # A* com métricas completas
│   └── heuristics.py         # Heurísticas (Manhattan, Euclidean, Chebyshev)
├── utils/                     # Utilitários compartilhados
│   ├── __init__.py
│   └── search.py             # SearchResult, funções auxiliares
├── results/                   # CSVs e resultados de experimentos
│   └── __init__.py
├── maze.py                    # Definição dos 9 labirintos
├── main.py                    # Interface interativa
└── run_experiments.py         # Execução e análise comparativa
```

## 🎮 Como Usar

### 1. Modo Interativo (Jogar)
Execute o menu interativo para escolher labirinto, algoritmo e heurística:

```bash
python main.py
```

**Funcionalidades:**
- Escolha entre 9 labirintos diferentes
- Selecione o algoritmo: DFS, BFS ou A*
- Para A*, escolha a heurística: Manhattan, Euclidean ou Chebyshev
- Visualize o caminho encontrado e métricas de desempenho

### 2. Experimentos Comparativos (Análise)
Execute comparação completa de todos algoritmos em todos labirintos:

```bash
python run_experiments.py
```

**Saída:**
- Tabelas comparativas no console
- CSV consolidado em `results/all_algorithms_comparison.csv`
- Métricas: tempo, nós visitados, nós gerados, tamanho da fronteira, custo do caminho

### 3. Teste de Integração
Valida que todos os arquivos estão presentes e funcionando:

```bash
bash test_integration.sh
```

**O que testa:**
- ✓ Estrutura de arquivos completa
- ✓ Experimentos executam sem erros
- ✓ CSV é gerado corretamente

## 📊 Métricas Coletadas

| Métrica | Descrição |
|---------|-----------|
| **time_s** | Tempo de execução (segundos) |
| **nodes_visited** | Nós expandidos durante a busca |
| **nodes_generated** | Total de nós gerados (apenas A*) |
| **max_frontier_size** | Tamanho máximo da fronteira (apenas A*) |
| **path_cost** | Custo total do caminho (apenas A*) |
| **path_length** | Número de movimentos até o objetivo |

## 🧮 Heurísticas do A*

### Manhattan (L1)
- **Uso**: Movimentos em 4 direções
- **Fórmula**: `|x₁-x₂| + |y₁-y₂|`
- **Características**: Admissível e consistente para grids sem diagonais

### Euclidean (L2)
- **Uso**: Movimentos em qualquer direção
- **Fórmula**: `√[(x₁-x₂)² + (y₁-y₂)²]`
- **Características**: Distância em linha reta

### Chebyshev (L∞)
- **Uso**: Movimentos diagonais com custo 1
- **Fórmula**: `max(|x₁-x₂|, |y₁-y₂|)`
- **Características**: Ideal quando diagonais custam igual a movimentos retos

## 🗺️ Labirintos Disponíveis

1. Pequeno e simples; caminho curto com poucos desvios
2. Pequeno com obstáculos moderados; alguns becos sem saída leves
3. Médio com múltiplas rotas possíveis e caminhos alternativos
4. Labirinto clássico com túneis e escolhas profundas
5. Linha reta; ideal para testar profundidade e performance mínima
6. Vários becos sem saída; ótimo para testar DFS vs BFS
7. Corredor longo e estreito; DFS tende a performar muito bem
8. Alta densidade de obstáculos; excelente para ver A* brilhar
9. Grande e complexo; ideal para comparar algoritmos em larga escala

## 📝 Entregáveis Atendidos

✅ **Código do A*** - Implementado em `search/astar.py`  
✅ **3 Heurísticas** - Manhattan, Euclidean, Chebyshev em `search/heuristics.py`  
✅ **Interface de escolha** - Menu interativo em `main.py`  
✅ **Funciona em labirintos** - Compatível com estrutura do projeto  
✅ **Registra métricas** - Tempo, nós, profundidade, custo, fronteira  
✅ **Resultados experimentais** - CSV em `results/all_algorithms_comparison.csv`

## 🔬 Exemplo de Análise

```python
# Executar experimento em labirinto específico
from run_experiments import run_experiment_on_maze

results = run_experiment_on_maze(maze_id=8, allow_diagonal=False)
```

## 👨‍💻 Autor

Projeto desenvolvido para disciplina de Inteligência Artificial - PUC
