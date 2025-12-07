# 🧩 Projeto: Métodos de Busca em Labirintos

Implementação e comparação de algoritmos de busca (DFS, BFS, Greedy Search e A*) aplicados a labirintos, com interface gráfica interativa para criação, edição e resolução de labirintos customizados.

## 📁 Estrutura do Projeto

```
study-ia_metodos_busca/
├── search/                          # Algoritmos de busca
│   ├── __init__.py
│   ├── dfs.py                      # Depth-First Search
│   ├── bfs.py                      # Breadth-First Search
│   ├── greedy_search_optimized.py  # Greedy Best-First Search
│   ├── astar.py                    # A* com métricas completas
│   └── heuristics.py               # Heurísticas (Manhattan, Euclidean, Chebyshev)
├── utils/                           # Utilitários compartilhados
│   ├── __init__.py
│   └── search.py                   # SearchResult, funções auxiliares
├── results/                         # CSVs e resultados de experimentos
│   ├── __init__.py
│   └── all_algorithms_comparison.csv
├── maze.py                          # Definição dos 9 labirintos padrão
├── maze_gui.py                      # Interface gráfica profissional
├── main.py                          # Launcher da GUI
└── run_experiments.py               # Execução e análise comparativa
```

## 🎮 Como Usar

### 1. Interface Gráfica Interativa (Recomendado)
Execute a interface gráfica profissional para criar, editar e resolver labirintos:

```bash
python main.py
```

**Funcionalidades da GUI:**

#### 🎨 Criação e Edição de Labirintos
- **Gerar labirinto aleatório** - Tamanhos: 10x10, 15x15, 20x20, 30x30 ou customizado (5-50)
- **Controle de densidade** - Ajuste a porcentagem de paredes (0-80%)
- **Edição interativa** - Desenhe paredes, espaços vazios, posição inicial e objetivo com o mouse
- **Labirinto padrão** - Carregue um labirinto pré-definido de exemplo
- **Garantia de solução** - Labirintos aleatórios sempre têm pelo menos um caminho válido

#### 🔍 Resolução Individual
- **8 algoritmos disponíveis:**
  - BFS (Busca em Largura)
  - DFS (Busca em Profundidade)
  - Greedy Search com 3 heurísticas (Manhattan, Euclidiana, Chebyshev)
  - A* com 3 heurísticas (Manhattan, Euclidiana, Chebyshev)
- **Animação visual** - Visualize a exploração passo a passo
- **Controle de velocidade** - Ajuste de Muito Rápido a Muito Lento
- **Métricas detalhadas** - Tempo, nós visitados, profundidade, custo do caminho

#### 🏆 Comparação de Algoritmos
- **"COMPARAR TODOS ALGORITMOS"** - Execute os 8 algoritmos simultaneamente
- **Visualização dividida** - Células compartilhadas são divididas entre algoritmos com cores distintas
- **Legenda dinâmica** - Identifique cada algoritmo pela cor
- **Análise comparativa automática** - Descubra qual foi mais rápido, eficiente e com melhor custo
- **Exportar resultados (CSV)** - Salve todos os resultados em formato compatível com análise

#### 📊 Estatísticas em Tempo Real
- Tamanho do labirinto (linhas x colunas)
- Total de células, paredes e espaços vazios
- Densidade de obstáculos

### 2. Experimentos Comparativos em Lote (Análise Científica)
Execute comparação completa de todos algoritmos nos 9 labirintos padrão:

```bash
python run_experiments.py
```

**Saída:**
- Tabelas comparativas no console
- CSV consolidado em `results/all_algorithms_comparison.csv`
- Métricas: tempo, nós visitados, nós gerados, tamanho da fronteira, custo do caminho, comprimento do caminho

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

| Métrica | Descrição | Algoritmos |
|---------|-----------|------------|
| **maze_id** | Identificador do labirinto | Todos |
| **algorithm** | Nome do algoritmo (DFS, BFS, Greedy, A*) | Todos |
| **heuristic** | Heurística utilizada (manhattan, euclidean, chebyshev, ou "-") | Greedy, A* |
| **path_found** | Se uma solução foi encontrada (True/False) | Todos |
| **time_s** | Tempo de execução em segundos | Todos |
| **nodes_visited** | Nós expandidos durante a busca | Todos |
| **nodes_generated** | Total de nós gerados | Greedy, A* |
| **max_frontier_size** | Tamanho máximo da fronteira | Greedy, A* |
| **path_cost** | Custo total do caminho | Greedy, A* |
| **path_length** | Número de movimentos até o objetivo | Todos |
| **depth** | Profundidade da solução encontrada | Todos |

## 🧮 Algoritmos Implementados

### DFS (Depth-First Search)
- **Estratégia**: Exploração em profundidade
- **Estrutura**: Pilha (LIFO)
- **Características**: Rápido, mas não garante caminho ótimo
- **Complexidade**: O(b^m) onde b = fator de ramificação, m = profundidade máxima

### BFS (Breadth-First Search)
- **Estratégia**: Exploração em largura
- **Estrutura**: Fila (FIFO)
- **Características**: Garante caminho ótimo em grafos não ponderados
- **Complexidade**: O(b^d) onde d = profundidade da solução

### Greedy Best-First Search
- **Estratégia**: Escolhe o nó mais próximo do objetivo segundo heurística
- **Estrutura**: Fila de prioridade (apenas h(n))
- **Características**: Rápido mas não garante caminho ótimo
- **Complexidade**: O(b^m) no pior caso

### A* (A-Star)
- **Estratégia**: Combina custo real g(n) e heurística h(n)
- **Estrutura**: Fila de prioridade (f(n) = g(n) + h(n))
- **Características**: Garante caminho ótimo se heurística for admissível
- **Complexidade**: O(b^d) com boa heurística

## 🎯 Heurísticas Disponíveis

### Manhattan (L1)
- **Uso**: Ideal para movimentos em 4 direções (cima, baixo, esquerda, direita)
- **Fórmula**: `|x₁-x₂| + |y₁-y₂|`
- **Características**: Admissível e consistente para grids sem diagonais
- **Vantagem**: Mais conservadora, explora sistematicamente

### Euclidean (L2)
- **Uso**: Distância em linha reta, qualquer direção
- **Fórmula**: `√[(x₁-x₂)² + (y₁-y₂)²]`
- **Características**: Distância real em espaço 2D
- **Vantagem**: Mais otimista, menos nós explorados quando aplicável

### Chebyshev (L∞)
- **Uso**: Movimentos diagonais com custo uniforme
- **Fórmula**: `max(|x₁-x₂|, |y₁-y₂|)`
- **Características**: Ideal quando diagonais custam igual a movimentos retos
- **Vantagem**: Melhor para grids com 8 direções de movimento

## 🗺️ Labirintos Disponíveis

### Labirintos Padrão (para experimentos)
Disponíveis em `maze.py` e utilizados por `run_experiments.py`:

1. **Pequeno e Simples** - Caminho curto com poucos desvios
2. **Obstáculos Moderados** - Pequeno com alguns becos sem saída leves
3. **Múltiplas Rotas** - Médio com caminhos alternativos
4. **Labirinto Clássico** - Túneis e escolhas profundas
5. **Linha Reta** - Ideal para testar profundidade e performance mínima
6. **Becos Sem Saída** - Ótimo para testar DFS vs BFS
7. **Corredor Estreito** - Longo e estreito, DFS tende a performar bem
8. **Alta Densidade** - Muitos obstáculos, excelente para ver A* brilhar
9. **Grande e Complexo** - Ideal para comparar algoritmos em larga escala

### Labirintos Customizados (GUI)
Na interface gráfica você pode:
- **Gerar aleatoriamente** com tamanhos de 5x5 até 50x50
- **Criar manualmente** desenhando paredes célula por célula
- **Editar qualquer labirinto** - modifique paredes, início e objetivo
- **Garantia de solução** - Algoritmo valida que existe caminho antes de finalizar

## 🎨 Visualização Comparativa

A GUI oferece modo de comparação que executa todos os 8 algoritmos simultaneamente:

- **Cores únicas**: Cada algoritmo tem uma cor distinta
- **Células divididas**: Quando múltiplos algoritmos passam pela mesma célula, ela é dividida em 2, 3, 4 ou mais partes
- **Legenda dinâmica**: Identifique cada algoritmo pela cor na legenda superior
- **Análise automática**: O sistema indica qual algoritmo foi:
  - ⚡ Mais rápido (menor tempo)
  - 💎 Melhor custo (menor custo de caminho)
  - 🎯 Mais eficiente (menos nós visitados)

## 🔬 Exemplos de Uso

### Executar experimento em labirinto específico
```python
from run_experiments import run_experiment_on_maze

# Testar todos algoritmos no labirinto 8
results = run_experiment_on_maze(maze_id=8, allow_diagonal=False)
```

### Usar algoritmos diretamente
```python
from search.bfs import bfs
from search.astar import astar
from search.heuristics import HEURISTICS
from maze import MAZES

# Resolver com BFS
result = bfs(MAZES[0], (0, 0), (4, 4))
print(f"Caminho encontrado: {result.found}")
print(f"Nós visitados: {result.nodes_visited}")
print(f"Tempo: {result.time:.6f}s")

# Resolver com A* usando Manhattan
result = astar(MAZES[0], (0, 0), (4, 4), HEURISTICS['manhattan'])
print(f"Custo do caminho: {result.path_cost}")
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Tkinter** - Interface gráfica
- **Threading** - Execução não-bloqueante na GUI
- **CSV** - Exportação e análise de dados
- **Collections** - Estruturas de dados eficientes (deque, heapq)

## 📦 Requisitos

```bash
# Instalação básica do Python 3.x (inclui Tkinter)
python --version  # Deve ser 3.6 ou superior
```

Não há dependências externas! Todos os módulos utilizados são da biblioteca padrão do Python.

## 🚀 Recursos Técnicos

### Validação de Labirintos
- **BFS para validação de caminhos** - Garante que labirintos aleatórios sempre têm solução
- **Tentativas múltiplas** - Até 100 tentativas para gerar labirinto válido
- **Criação de caminho garantido** - Fallback que conecta início ao objetivo

### Performance
- **Threading** - Interface não trava durante execução de algoritmos
- **Animação suave** - Controle de velocidade com sleep ajustável
- **Canvas otimizado** - Redesenho eficiente com cálculo dinâmico de tamanho

### Interface Profissional
- **Tema moderno** - Paleta de cores Dark Mode com acentos vibrantes
- **Layout responsivo** - Redimensionamento automático do canvas
- **Scroll** - Painel de controle com scroll para telas menores
- **Estatísticas em tempo real** - Atualização dinâmica de métricas

## 📈 Formato do CSV Exportado

O arquivo CSV gerado pela comparação segue o formato:

```csv
maze_id,algorithm,heuristic,path_found,time_s,nodes_visited,nodes_generated,max_frontier_size,path_cost,path_length
1,BFS,-,True,0.000031,13,-,-,-,7
1,Greedy,manhattan,True,0.000036,9,12,4,7.0,7
1,A*,manhattan,True,0.000060,12,13,2,7.0,7
```

Compatível com análise em Python (Pandas), Excel, R, etc.

## 👨‍💻 Autor

- **Maria Almeida**  

- **Laura Menezes**

- **Gustavo Henrique**

- **Felipe Ratton**

- **Alice Salim**

Projeto desenvolvido para disciplina de Inteligência Artificial - PUC

## 📄 Licença

Este projeto é de uso educacional e acadêmico.
