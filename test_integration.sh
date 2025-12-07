#!/bin/bash
# test_integration.sh
# Script para testar a integração completa do projeto

echo "=========================================="
echo "TESTE DE INTEGRAÇÃO - MÉTODOS DE BUSCA"
echo "=========================================="
echo ""

# Teste 1: Verificar estrutura de arquivos
echo "✓ Verificando estrutura de arquivos..."
required_files=(
    "main.py"
    "maze.py"
    "run_experiments.py"
    "search/astar.py"
    "search/bfs.py"
    "search/dfs.py"
    "search/heuristics.py"
    "utils/search.py"
    "README.md"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file - FALTANDO!"
        exit 1
    fi
done

echo ""
echo "✓ Todos os arquivos necessários estão presentes!"
echo ""

# Teste 2: Executar experimentos
echo "✓ Executando experimentos comparativos..."
python run_experiments.py > test_output.log 2>&1

if [ -f "results/all_algorithms_comparison.csv" ]; then
    echo "  ✓ run_experiments.py executado com sucesso!"
    rm -f test_output.log
else
    echo "  ✗ Erro ao executar run_experiments.py"
    cat test_output.log
    exit 1
fi

# Teste 3: Verificar CSV gerado
if [ -f "results/all_algorithms_comparison.csv" ]; then
    lines=$(wc -l < "results/all_algorithms_comparison.csv")
    echo "  ✓ CSV gerado com $lines linhas"
else
    echo "  ✗ CSV não foi gerado!"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ TODOS OS TESTES PASSARAM!"
echo "=========================================="
echo ""
echo "Estrutura final do projeto:"
find . -type d -not -path '*/\.*' -not -path '*/__pycache__*' -not -path '*/.*' | head -20

echo ""
echo "Para usar o projeto:"
echo "  1. python main.py           # Modo interativo"
echo "  2. python run_experiments.py # Análise comparativa"
