"""
Advanced Maze Solver - Graphical User Interface
Professional interface for creating, editing, and solving mazes with multiple search algorithms
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import csv
from typing import List, Tuple, Optional
from maze import get_start_and_goal
from search.dfs import dfs
from search.bfs import bfs
from search.greedy_search_optimized import greedy_search
from search.astar import astar
from search.heuristics import HEURISTICS


class MazeGUI:
    """Professional maze solver with advanced visualization and editing capabilities."""
    
    def __init__(self, root):
        """Initialize the graphical interface."""
        self.root = root
        self.root.title("Resolvedor Avançado de Labirintos - Ferramenta de Comparação de Algoritmos")
        self.root.geometry("1600x950")
        self.root.minsize(1400, 800)
        
        self.maze_grid = None
        self.start_pos = None
        self.goal_pos = None
        self.current_result = None
        self.cell_size = 30
        self.is_solving = False
        self.is_animating = False
        self.animation_speed = 50  # ms
        self.stop_event = threading.Event()
        
        self.edit_mode = tk.StringVar(value="wall")  # wall, start, goal, empty
        self.drawing = False
        
        # Para comparação de múltiplos algoritmos
        self.all_results = {}  # Armazena resultados de todos os algoritmos
        self.comparison_mode = False  # Modo de visualização comparativa
        
        # Modern color scheme
        self.COLORS = {
            'wall': '#1a1a2e',           # Dark blue-black for walls
            'path': '#ff6b6b',           # Coral red for solution path
            'start': '#06ffa5',          # Bright cyan for start
            'goal': '#ffd93d',           # Bright yellow for goal
            'empty': '#f8f9fa',          # Light gray for empty cells
            'visited': '#4ecdc4',        # Turquoise for visited nodes
            'frontier': '#a8dadc',       # Light blue for frontier
            'bg': '#16213e',             # Dark background
            'panel': '#1a1a2e',          # Panel background
            'text': '#f8f9fa',           # Light text
            'highlight': '#e63946'       # Accent color
        }
        
        # Cores para comparação de algoritmos (8 cores distintas)
        self.ALGORITHM_COLORS = [
            '#FF6B6B',  # Vermelho
            '#4ECDC4',  # Turquesa
            '#95E1D3',  # Verde água
            '#FFD93D',  # Amarelo
            '#6BCF7F',  # Verde
            '#A78BFA',  # Roxo
            '#F472B6',  # Rosa
            '#FB923C',  # Laranja
        ]
        
        self._setup_style()
        
        self._create_widgets()
        
        self._create_default_maze()
        self._draw_maze()
    
    def _setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        

        style.configure('TFrame', background=self.COLORS['panel'])
        style.configure('TLabel', background=self.COLORS['panel'], 
                       foreground=self.COLORS['text'], font=('Segoe UI', 10))
        style.configure('Title.TLabel', font=('Segoe UI', 14, 'bold'))
        style.configure('Header.TLabel', font=('Segoe UI', 11, 'bold'))
        
        style.configure('TButton', font=('Segoe UI', 10), padding=8)
        style.configure('Solve.TButton', font=('Segoe UI', 12, 'bold'), padding=10)
        
        style.configure('TRadiobutton', background=self.COLORS['panel'],
                       foreground=self.COLORS['text'], font=('Segoe UI', 10))
        

        style.configure('TLabelframe', background=self.COLORS['panel'],
                       foreground=self.COLORS['text'])
        style.configure('TLabelframe.Label', background=self.COLORS['panel'],
                       foreground=self.COLORS['text'], font=('Segoe UI', 11, 'bold'))
    
    def _create_widgets(self):

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        left_panel = self._create_left_panel(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        right_panel = self._create_right_panel(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def _create_left_panel(self, parent):
        panel = ttk.Frame(parent)
        
        canvas = tk.Canvas(panel, bg=self.COLORS['panel'], width=320, 
                          highlightthickness=0)
        scrollbar = ttk.Scrollbar(panel, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        

        title = ttk.Label(scrollable_frame, text="PAINEL DE CONTROLE", 
                         style='Title.TLabel')
        title.pack(pady=(10, 15))
        
        self._create_size_section(scrollable_frame)
        
        self._create_density_section(scrollable_frame)
        
        self._create_generation_section(scrollable_frame)
        
        self._create_edit_section(scrollable_frame)
        
        self._create_algorithm_section(scrollable_frame)
        
        self._create_solver_section(scrollable_frame)
        
        self._create_animation_section(scrollable_frame)
        
        self._create_results_section(scrollable_frame)
        
        self._create_file_section(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return panel
    
    def _create_size_section(self, parent):
        """Create maze size selection section."""
        frame = ttk.LabelFrame(parent, text="Configuração do Tamanho", padding=10)
        frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.size_var = tk.StringVar(value="15")
        
        sizes = [
            ("Pequeno (10x10)", "10"),
            ("Médio (15x15)", "15"),
            ("Grande (20x20)", "20"),
            ("Extra Grande (30x30)", "30"),
        ]
        
        for text, value in sizes:
            ttk.Radiobutton(frame, text=text, variable=self.size_var, 
                          value=value).pack(anchor=tk.W, pady=2)
        
        custom_frame = ttk.Frame(frame)
        custom_frame.pack(anchor=tk.W, pady=(5, 0))
        ttk.Radiobutton(custom_frame, text="Tamanho Customizado:", 
                       variable=self.size_var, value="custom").pack(side=tk.LEFT)
        
        self.custom_size_entry = ttk.Entry(custom_frame, width=6)
        self.custom_size_entry.pack(side=tk.LEFT, padx=(5, 0))
        self.custom_size_entry.insert(0, "15")
    
    def _create_density_section(self, parent):
        """Create wall density control section."""
        frame = ttk.LabelFrame(parent, text="Controle de Densidade de Paredes", padding=10)
        frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.density_var = tk.DoubleVar(value=0.25)
        density_scale = ttk.Scale(frame, from_=0.0, to=0.6, 
                                 variable=self.density_var, orient=tk.HORIZONTAL)
        density_scale.pack(fill=tk.X, pady=(0, 5))
        
        self.density_label = ttk.Label(frame, text="25%")
        self.density_label.pack()
        density_scale.configure(command=self._update_density_label)
    
    def _create_generation_section(self, parent):
        """Create maze generation buttons section."""
        frame = ttk.LabelFrame(parent, text="Geração de Labirinto", padding=10)
        frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(frame, text="Gerar Labirinto Aleatório", 
                  command=self._generate_random_maze).pack(fill=tk.X, pady=2)
        ttk.Button(frame, text="Carregar Labirinto Padrão", 
                  command=self._create_default_maze).pack(fill=tk.X, pady=2)
        ttk.Button(frame, text="Limpar Tudo", 
                  command=self._clear_maze).pack(fill=tk.X, pady=2)
    
    def _create_edit_section(self, parent):
        """Create editing tools section."""
        frame = ttk.LabelFrame(parent, text="Ferramentas de Edição", padding=10)
        frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tools = [
            ("[PAREDE] Desenhar Parede", "wall"),
            ("[VAZIO] Desenhar Espaço Vazio", "empty"),
            ("[INÍCIO] Definir Posição Inicial", "start"),
            ("[META] Definir Posição do Objetivo", "goal"),
        ]
        
        for text, value in tools:
            ttk.Radiobutton(frame, text=text, variable=self.edit_mode, 
                          value=value).pack(anchor=tk.W, pady=2)
        
        info = ttk.Label(frame, text="Clique e arraste no labirinto\npara editar células",
                        font=('Segoe UI', 9, 'italic'))
        info.pack(pady=(10, 0))
    
    def _create_algorithm_section(self, parent):
        """Create search algorithm selection section."""
        frame = ttk.LabelFrame(parent, text="Seleção de Algoritmo de Busca", padding=10)
        frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.algo_var = tk.StringVar(value="bfs")
        
        algorithms = [
            ("[BFS] Busca em Largura", "bfs"),
            ("[DFS] Busca em Profundidade", "dfs"),
            ("[GULOSO] Guloso - Heurística Manhattan", "greedy_manhattan"),
            ("[GULOSO] Guloso - Heurística Euclidiana", "greedy_euclidean"),
            ("[GULOSO] Guloso - Heurística Chebyshev", "greedy_chebyshev"),
            ("[A*] A-Estrela - Heurística Manhattan", "astar_manhattan"),
            ("[A*] A-Estrela - Heurística Euclidiana", "astar_euclidean"),
            ("[A*] A-Estrela - Heurística Chebyshev", "astar_chebyshev"),
        ]
        
        for text, value in algorithms:
            ttk.Radiobutton(frame, text=text, variable=self.algo_var, 
                          value=value).pack(anchor=tk.W, pady=2)
    
    def _create_solver_section(self, parent):
        """Create solver controls section."""
        frame = ttk.LabelFrame(parent, text="Controles de Resolução", padding=10)
        frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.solve_button = ttk.Button(frame, text="RESOLVER LABIRINTO", 
                                       style='Solve.TButton',
                                       command=self._solve_maze)
        self.solve_button.pack(fill=tk.X, pady=5)
        
        self.compare_button = ttk.Button(frame, text="COMPARAR TODOS ALGORITMOS", 
                                        style='Solve.TButton',
                                        command=self._compare_all_algorithms)
        self.compare_button.pack(fill=tk.X, pady=5)
        
        self.stop_button = ttk.Button(frame, text="PARAR", 
                                      command=self._stop_solving,
                                      state=tk.DISABLED)
        self.stop_button.pack(fill=tk.X, pady=5)
        
        ttk.Button(frame, text="Limpar Solução", 
                  command=self._clear_solution).pack(fill=tk.X, pady=5)
    
    def _create_animation_section(self, parent):
        """Create animation speed control section."""
        frame = ttk.LabelFrame(parent, text="Velocidade da Animação", padding=10)
        frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.speed_var = tk.IntVar(value=50)
        speed_scale = ttk.Scale(frame, from_=10, to=200, 
                               variable=self.speed_var, orient=tk.HORIZONTAL)
        speed_scale.pack(fill=tk.X, pady=(0, 5))
        
        self.speed_label = ttk.Label(frame, text="Normal")
        self.speed_label.pack()
        speed_scale.configure(command=self._update_speed_label)
    
    def _create_results_section(self, parent):
        """Create results display section."""
        frame = ttk.LabelFrame(parent, text="Métricas e Resultados do Algoritmo", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_text = tk.Text(text_frame, height=12, width=35, 
                                    state=tk.DISABLED, wrap=tk.WORD,
                                    bg='#1E1E1E', fg='#F8F8F2',
                                    font=('Consolas', 9),
                                    yscrollcommand=scrollbar.set)
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.results_text.yview)
    
    def _create_file_section(self, parent):
        """Create file operations section."""
        frame = ttk.LabelFrame(parent, text="Exportar Resultados", padding=10)
        frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.export_button = ttk.Button(frame, text="Exportar Resultados (CSV)", 
                                       command=self._export_results,
                                       state=tk.DISABLED)
        self.export_button.pack(fill=tk.X, pady=2)
    
    def _create_right_panel(self, parent):
        """Create visualization panel."""
        panel = ttk.Frame(parent)
        
        header = ttk.Frame(panel)
        header.pack(fill=tk.X, pady=(0, 5))
        
        title = ttk.Label(header, text="VISUALIZAÇÃO DO LABIRINTO", 
                         style='Title.TLabel')
        title.pack(side=tk.LEFT, padx=10)
        
        # Add statistics display
        self.stats_label = ttk.Label(header, text="", font=('Segoe UI', 9))
        self.stats_label.pack(side=tk.LEFT, padx=20)
        
        # Frame para legendas (será atualizado dinamicamente)
        self.legend_frame = ttk.Frame(header)
        self.legend_frame.pack(side=tk.RIGHT, padx=10)
        
        self._update_legend()
        
        canvas_frame = ttk.Frame(panel)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg=self.COLORS['empty'], 
                               highlightthickness=2, highlightbackground=self.COLORS['bg'])
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<B1-Motion>", self._on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_canvas_release)
        
        self.root.bind("<Configure>", self._on_resize)
        
        return panel
    
    def _update_density_label(self, value):
        density = float(value)
        self.density_label.config(text=f"{int(density * 100)}%")
    
    def _update_speed_label(self, value):
        speed = int(float(value))
        self.animation_speed = speed
        if speed < 30:
            label = "Muito Rápido"
        elif speed < 70:
            label = "Rápido"
        elif speed < 110:
            label = "Normal"
        elif speed < 150:
            label = "Lento"
        else:
            label = "Muito Lento"
        self.speed_label.config(text=label)
    
    def _get_maze_size(self):
        size_choice = self.size_var.get()
        
        if size_choice == "custom":
            try:
                size = int(self.custom_size_entry.get())
                if size < 5 or size > 50:
                    messagebox.showerror("Erro", "Tamanho deve estar entre 5 e 50.")
                    return None
                return size
            except ValueError:
                messagebox.showerror("Erro", "Tamanho inválido.")
                return None
        else:
            return int(size_choice)
    
    def _create_default_maze(self):
        size = 15
        self.maze_grid = [[0 for _ in range(size)] for _ in range(size)]
        self.start_pos = (0, 0)
        self.goal_pos = (size - 1, size - 1)
        
        for i in range(3, 12):
            self.maze_grid[i][7] = 1
        for i in range(3, 10):
            self.maze_grid[5][i] = 1
        
        self.current_result = None
        self._draw_maze()
        self._clear_results()
    
    def _generate_random_maze(self):
        if self.is_solving:
            messagebox.showwarning("Aviso", "Aguarde o término da resolução atual.")
            return
        
        size = self._get_maze_size()
        if size is None:
            return
        
        density = self.density_var.get()
        
        import random
        from collections import deque
        
        max_attempts = 100
        for attempt in range(max_attempts):
            self.maze_grid = [[0 for _ in range(size)] for _ in range(size)]
            
            for i in range(size):
                for j in range(size):
                    if random.random() < density:
                        self.maze_grid[i][j] = 1
            
            self.start_pos = (0, 0)
            self.goal_pos = (size - 1, size - 1)
            self.maze_grid[0][0] = 0
            self.maze_grid[size-1][size-1] = 0
            
            if self._has_path(self.start_pos, self.goal_pos):
                break

            if attempt == max_attempts - 1:
                self._create_guaranteed_path()
        
        self.current_result = None
        self._draw_maze()
        self._clear_results()
    
    def _has_path(self, start, goal):

        from collections import deque
        
        rows = len(self.maze_grid)
        cols = len(self.maze_grid[0])
        
        queue = deque([start])
        visited = {start}
        
        while queue:
            r, c = queue.popleft()
            
            if (r, c) == goal:
                return True
            
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                
                if (0 <= nr < rows and 0 <= nc < cols and 
                    (nr, nc) not in visited and self.maze_grid[nr][nc] == 0):
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        
        return False
    
    def _create_guaranteed_path(self):
        import random
        
        rows = len(self.maze_grid)
        cols = len(self.maze_grid[0])
        
        r, c = self.start_pos
        goal_r, goal_c = self.goal_pos

        while c < goal_c:
            self.maze_grid[r][c] = 0
            c += 1

            if random.random() < 0.3 and r < goal_r:
                r += 1
            elif random.random() < 0.3 and r > 0:
                r -= 1
            r = max(0, min(rows - 1, r))
        

        while r < goal_r:
            self.maze_grid[r][c] = 0
            r += 1
        
        while r > goal_r:
            self.maze_grid[r][c] = 0
            r -= 1
        

        self.maze_grid[goal_r][goal_c] = 0
    
    def _clear_maze(self):

        if self.is_solving:
            messagebox.showwarning("Aviso", "Aguarde o término da resolução atual.")
            return
        
        size = self._get_maze_size()
        if size is None:
            size = 15
        
        self.maze_grid = [[0 for _ in range(size)] for _ in range(size)]
        self.start_pos = (0, 0)
        self.goal_pos = (size - 1, size - 1)
        self.current_result = None
        self._draw_maze()
        self._clear_results()
    
    def _on_canvas_click(self, event):

        if self.is_solving:
            return
        
        self.drawing = True
        self._edit_cell(event.x, event.y)
    
    def _on_canvas_drag(self, event):

        if self.is_solving or not self.drawing:
            return
        
        self._edit_cell(event.x, event.y)
    
    def _on_canvas_release(self, event):
        self.drawing = False
    
    def _edit_cell(self, x, y):

        if not self.maze_grid:
            return
        

        self.canvas.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        rows = len(self.maze_grid)
        cols = len(self.maze_grid[0])
        
        cell_size_w = max(10, (canvas_width - 20) // cols)
        cell_size_h = max(10, (canvas_height - 20) // rows)
        cell_size = min(cell_size_w, cell_size_h)
        
        total_width = cols * cell_size
        total_height = rows * cell_size
        offset_x = (canvas_width - total_width) // 2
        offset_y = (canvas_height - total_height) // 2
        
        col = (x - offset_x) // cell_size
        row = (y - offset_y) // cell_size
        
        if 0 <= row < rows and 0 <= col < cols:
            mode = self.edit_mode.get()
            
            if mode == "wall":
                if (row, col) != self.start_pos and (row, col) != self.goal_pos:
                    self.maze_grid[row][col] = 1
            elif mode == "empty":
                if (row, col) != self.start_pos and (row, col) != self.goal_pos:
                    self.maze_grid[row][col] = 0
            elif mode == "start":
                self.maze_grid[self.start_pos[0]][self.start_pos[1]] = 0
                self.start_pos = (row, col)
                self.maze_grid[row][col] = 0
            elif mode == "goal":
                self.maze_grid[self.goal_pos[0]][self.goal_pos[1]] = 0
                self.goal_pos = (row, col)
                self.maze_grid[row][col] = 0
            
            self._draw_maze()
    
    def _on_resize(self, event):
        if event.widget == self.root and self.maze_grid:
            self._draw_maze()
    
    def _draw_maze(self, path_to_draw=None, visited_to_draw=None):
        """Draw the maze on canvas with current state."""
        self.canvas.delete("all")
        
        if not self.maze_grid:
            return
        
        # Se estamos em modo de comparação, usar o método específico
        if self.comparison_mode and not path_to_draw and not visited_to_draw:
            self._draw_comparison()
            return
        
        # Update statistics
        self._update_stats()
        

        self.canvas.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            return
        
        rows = len(self.maze_grid)
        cols = len(self.maze_grid[0])
        
        cell_size_w = max(10, (canvas_width - 20) // cols)
        cell_size_h = max(10, (canvas_height - 20) // rows)
        self.cell_size = min(cell_size_w, cell_size_h)
        
        total_width = cols * self.cell_size
        total_height = rows * self.cell_size
        offset_x = (canvas_width - total_width) // 2
        offset_y = (canvas_height - total_height) // 2
        
        path_set = set(path_to_draw) if path_to_draw else set()
        visited_set = set(visited_to_draw) if visited_to_draw else set()
        
        if self.current_result and not path_to_draw and not visited_to_draw:
            if self.current_result.found:
                path_set = set(self.current_result.path)
            if hasattr(self.current_result, 'visited_nodes'):
                visited_set = self.current_result.visited_nodes
        
        for row in range(rows):
            for col in range(cols):
                x1 = offset_x + col * self.cell_size
                y1 = offset_y + row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                pos = (row, col)
                
                color = self.COLORS['empty']
                
                if self.maze_grid[row][col] == 1:
                    color = self.COLORS['wall']
                elif pos in visited_set:
                    color = self.COLORS['visited']
                
                if pos in path_set and pos != self.start_pos and pos != self.goal_pos:
                    color = self.COLORS['path']
                
                if pos == self.start_pos:
                    color = self.COLORS['start']
                elif pos == self.goal_pos:
                    color = self.COLORS['goal']
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, 
                                            outline='#95A5A6', width=1)
                
                if pos == self.start_pos and self.cell_size > 15:
                    self.canvas.create_text((x1+x2)//2, (y1+y2)//2, 
                                          text="S", fill="white", 
                                          font=('Arial', max(8, self.cell_size//2), 'bold'))
                elif pos == self.goal_pos and self.cell_size > 15:
                    self.canvas.create_text((x1+x2)//2, (y1+y2)//2, 
                                          text="G", fill="white", 
                                          font=('Arial', max(8, self.cell_size//2), 'bold'))
    
    def _update_stats(self):
        """Update maze statistics display."""
        if self.maze_grid:
            rows = len(self.maze_grid)
            cols = len(self.maze_grid[0])
            total_cells = rows * cols
            wall_cells = sum(row.count(1) for row in self.maze_grid)
            empty_cells = total_cells - wall_cells
            density = (wall_cells / total_cells) * 100
            
            stats = f"Tamanho: {rows}x{cols} | Células: {total_cells} | Paredes: {wall_cells} ({density:.1f}%) | Vazias: {empty_cells}"
            self.stats_label.config(text=stats)
    
    def _update_legend(self):
        """Atualiza a legenda de acordo com o modo atual."""
        # Limpar legenda atual
        for widget in self.legend_frame.winfo_children():
            widget.destroy()
        
        if self.comparison_mode and self.all_results:
            # Modo comparação - mostrar cores dos algoritmos
            for idx, algo_name in enumerate(self.all_results.keys()):
                color = self.ALGORITHM_COLORS[idx % len(self.ALGORITHM_COLORS)]
                
                # Criar um canvas pequeno para o quadrado de cor
                color_canvas = tk.Canvas(self.legend_frame, width=12, height=12, 
                                        bg=self.COLORS['panel'], highlightthickness=0)
                color_canvas.pack(side=tk.LEFT, padx=(5, 2))
                color_canvas.create_rectangle(1, 1, 11, 11, fill=color, outline='black', width=1)
                
                # Nome do algoritmo
                lbl = ttk.Label(self.legend_frame, text=algo_name, font=('Segoe UI', 8))
                lbl.pack(side=tk.LEFT, padx=(0, 8))
        else:
            # Modo normal - legenda padrão
            legends = [
                ("[INÍCIO] Início", self.COLORS['start']),
                ("[META] Objetivo", self.COLORS['goal']),
                ("[VISITADO] Visitado", self.COLORS['visited']),
                ("[CAMINHO] Caminho da Solução", self.COLORS['path']),
            ]
            
            for text, color in legends:
                lbl = ttk.Label(self.legend_frame, text=text, font=('Segoe UI', 9))
                lbl.pack(side=tk.LEFT, padx=5)
    
    def _solve_maze(self):
        """Solve the maze using selected algorithm."""
        if self.is_solving:
            messagebox.showwarning("Aviso", "Uma solução já está em andamento.")
            return
        
        if not self.maze_grid or not self.start_pos or not self.goal_pos:
            messagebox.showerror("Erro", "Configuração de labirinto inválida.")
            return

        self.stop_event.clear()
        

        thread = threading.Thread(target=self._solve_thread)
        thread.daemon = True
        thread.start()
    
    def _solve_thread(self):

        self.is_solving = True
        self.solve_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        try:

            maze = [[1 if cell == 1 else 0 for cell in row] for row in self.maze_grid]
            maze[self.start_pos[0]][self.start_pos[1]] = 'S'
            maze[self.goal_pos[0]][self.goal_pos[1]] = 'G'
            
            algo_choice = self.algo_var.get()
            

            if algo_choice == "bfs":
                result = bfs(maze, self.start_pos, self.goal_pos)
                algo_name = "BFS - Busca em Largura"
            elif algo_choice == "dfs":
                result = dfs(maze, self.start_pos, self.goal_pos)
                algo_name = "DFS - Busca em Profundidade"
            elif algo_choice.startswith("greedy_"):
                heur_type = algo_choice.split("_")[1]
                heur_func = HEURISTICS[heur_type]
                result = greedy_search(maze, self.start_pos, self.goal_pos, heur_func)
                algo_name = f"Greedy - {heur_type.capitalize()}"
            elif algo_choice.startswith("astar_"):
                heur_type = algo_choice.split("_")[1]
                heur_func = HEURISTICS[heur_type]
                result = astar(maze, self.start_pos, self.goal_pos, heur_func, allow_diagonal=False)
                algo_name = f"A* - {heur_type.capitalize()}"
            else:
                return
            
            self.current_result = result
            self._display_results(algo_name, result)
            

            if result.found and not self.stop_event.is_set():
                self._animate_solution(result)
            else:
                self._draw_maze()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao resolver labirinto: {str(e)}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.is_solving = False
            self.is_animating = False
            self.solve_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def _animate_solution(self, result):

        self.is_animating = True
        

        visited_list = list(result.visited_nodes) if hasattr(result, 'visited_nodes') else []
        
        for i, node in enumerate(visited_list):
            if self.stop_event.is_set():
                break
            self._draw_maze(visited_to_draw=visited_list[:i+1])
            self.root.update()
            time.sleep(self.animation_speed / 1000.0)

        if result.found and not self.stop_event.is_set():
            for i in range(len(result.path)):
                if self.stop_event.is_set():
                    break
                self._draw_maze(path_to_draw=result.path[:i+1], 
                               visited_to_draw=visited_list)
                self.root.update()
                time.sleep(self.animation_speed / 1000.0)
        

        if not self.stop_event.is_set():
            self._draw_maze()
        
        self.is_animating = False
    
    def _stop_solving(self):

        self.stop_event.set()
        self.is_solving = False
        self.is_animating = False
        self.solve_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def _clear_solution(self):

        if self.is_solving or self.is_animating:
            return
        
        self.current_result = None
        self.all_results = {}
        self.comparison_mode = False
        self.export_button.config(state=tk.DISABLED)
        self._update_legend()
        self._draw_maze()
        self._clear_results()
    
    def _display_results(self, algo_name, result):

        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        text = f"{'='*35}\n"
        text += f"ALGORITMO: {algo_name}\n"
        text += f"{'='*35}\n\n"
        
        if result.found:
            text += "✓ SOLUÇÃO ENCONTRADA!\n\n"
            text += f"📏 Profundidade: {result.depth}\n"
            text += f"👣 Nós Visitados: {result.nodes_visited}\n"
            
            if hasattr(result, 'nodes_generated') and result.nodes_generated:
                text += f"Nós Gerados: {result.nodes_generated}\n"
            
            if hasattr(result, 'max_frontier_size') and result.max_frontier_size:
                text += f"Fronteira Máx: {result.max_frontier_size}\n"
            
            if hasattr(result, 'path_cost') and result.path_cost is not None:
                text += f"Custo do Caminho: {result.path_cost}\n"
            
            text += f"Tempo: {result.time:.6f}s\n"
            text += f"Tempo: {result.time*1000:.2f}ms\n"
        else:
            text += "✗ SOLUÇÃO NÃO ENCONTRADA!\n\n"
            text += f"Nós Visitados: {result.nodes_visited}\n"
            text += f"Tempo: {result.time:.6f}s\n"
        
        self.results_text.insert(tk.END, text)
        self.results_text.config(state=tk.DISABLED)
    
    def _clear_results(self):
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
    
    def _compare_all_algorithms(self):
        """Executa todos os algoritmos e compara os resultados."""
        if self.is_solving:
            messagebox.showwarning("Aviso", "Uma solução já está em andamento.")
            return
        
        if not self.maze_grid or not self.start_pos or not self.goal_pos:
            messagebox.showerror("Erro", "Configuração de labirinto inválida.")
            return
        
        self.stop_event.clear()
        self.is_solving = True
        self.solve_button.config(state=tk.DISABLED)
        self.compare_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        def run_comparison():
            try:
                self.all_results = {}
                
                # Lista de todos os algoritmos
                algorithms = [
                    ("BFS", lambda: bfs(self.maze_grid, self.start_pos, self.goal_pos)),
                    ("DFS", lambda: dfs(self.maze_grid, self.start_pos, self.goal_pos)),
                    ("Guloso (Manhattan)", lambda: greedy_search(self.maze_grid, self.start_pos, self.goal_pos, HEURISTICS['manhattan'])),
                    ("Guloso (Euclidiana)", lambda: greedy_search(self.maze_grid, self.start_pos, self.goal_pos, HEURISTICS['euclidean'])),
                    ("Guloso (Chebyshev)", lambda: greedy_search(self.maze_grid, self.start_pos, self.goal_pos, HEURISTICS['chebyshev'])),
                    ("A* (Manhattan)", lambda: astar(self.maze_grid, self.start_pos, self.goal_pos, HEURISTICS['manhattan'])),
                    ("A* (Euclidiana)", lambda: astar(self.maze_grid, self.start_pos, self.goal_pos, HEURISTICS['euclidean'])),
                    ("A* (Chebyshev)", lambda: astar(self.maze_grid, self.start_pos, self.goal_pos, HEURISTICS['chebyshev'])),
                ]
                
                for algo_name, algo_func in algorithms:
                    if self.stop_event.is_set():
                        break
                    
                    result = algo_func()
                    self.all_results[algo_name] = result
                    
                    # Mostrar progresso
                    self.root.after(0, lambda name=algo_name: self._update_comparison_progress(name))
                
                if not self.stop_event.is_set():
                    self.comparison_mode = True
                    self.root.after(0, self._update_legend)
                    self.root.after(0, self._draw_comparison)
                    self.root.after(0, self._display_comparison_results)
                    self.root.after(0, lambda: self.export_button.config(state=tk.NORMAL))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro na comparação: {str(e)}"))
            finally:
                self.is_solving = False
                self.root.after(0, lambda: self.solve_button.config(state=tk.NORMAL))
                self.root.after(0, lambda: self.compare_button.config(state=tk.NORMAL))
                self.root.after(0, lambda: self.stop_button.config(state=tk.DISABLED))
        
        thread = threading.Thread(target=run_comparison, daemon=True)
        thread.start()
    
    def _update_comparison_progress(self, algo_name):
        """Atualiza o texto de progresso durante a comparação."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.insert(tk.END, f"✓ {algo_name}\n")
        self.results_text.see(tk.END)
        self.results_text.config(state=tk.DISABLED)
    
    def _draw_comparison(self):
        """Desenha o labirinto com todos os caminhos de solução comparados."""
        if not self.maze_grid or not self.all_results:
            return
        
        rows = len(self.maze_grid)
        cols = len(self.maze_grid[0])
        
        # Calcular tamanho das células
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 800
            canvas_height = 800
        
        self.cell_size = min(canvas_width // cols, canvas_height // rows, 50)
        
        self.canvas.delete("all")
        
        # Criar um dicionário para mapear células aos algoritmos que as visitam
        cell_algorithms = {}  # (row, col) -> [list of algorithm indices]
        
        algo_list = list(self.all_results.keys())
        
        for algo_idx, (algo_name, result) in enumerate(self.all_results.items()):
            if result.found and result.path:
                for pos in result.path:
                    if pos not in cell_algorithms:
                        cell_algorithms[pos] = []
                    cell_algorithms[pos].append(algo_idx)
        
        # Desenhar células
        for row in range(rows):
            for col in range(cols):
                pos = (row, col)
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Determinar cor base
                if self.maze_grid[row][col] == 1:
                    color = self.COLORS['wall']
                elif pos == self.start_pos:
                    color = self.COLORS['start']
                elif pos == self.goal_pos:
                    color = self.COLORS['goal']
                elif pos in cell_algorithms:
                    # Célula visitada por um ou mais algoritmos
                    algo_indices = cell_algorithms[pos]
                    
                    if len(algo_indices) == 1:
                        # Apenas um algoritmo - usar cor sólida
                        color = self.ALGORITHM_COLORS[algo_indices[0] % len(self.ALGORITHM_COLORS)]
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='#95A5A6', width=1)
                    else:
                        # Múltiplos algoritmos - dividir a célula
                        self._draw_divided_cell(x1, y1, x2, y2, algo_indices)
                    continue
                else:
                    color = self.COLORS['empty']
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='#95A5A6', width=1)
                
                # Adicionar marcadores S e G
                if pos == self.start_pos and self.cell_size > 15:
                    self.canvas.create_text((x1+x2)//2, (y1+y2)//2, 
                                          text="S", fill="white", 
                                          font=('Arial', max(8, self.cell_size//2), 'bold'))
                elif pos == self.goal_pos and self.cell_size > 15:
                    self.canvas.create_text((x1+x2)//2, (y1+y2)//2, 
                                          text="G", fill="white", 
                                          font=('Arial', max(8, self.cell_size//2), 'bold'))
        
        self._update_stats()
    
    def _draw_divided_cell(self, x1, y1, x2, y2, algo_indices):
        """Divide uma célula entre múltiplos algoritmos."""
        num_algos = len(algo_indices)
        
        if num_algos == 2:
            # Dividir diagonalmente
            colors = [self.ALGORITHM_COLORS[idx % len(self.ALGORITHM_COLORS)] for idx in algo_indices]
            # Triângulo superior esquerdo
            self.canvas.create_polygon(x1, y1, x2, y1, x1, y2, fill=colors[0], outline='#95A5A6', width=1)
            # Triângulo inferior direito
            self.canvas.create_polygon(x2, y1, x2, y2, x1, y2, fill=colors[1], outline='#95A5A6', width=1)
        
        elif num_algos == 3:
            # Dividir em três triângulos
            colors = [self.ALGORITHM_COLORS[idx % len(self.ALGORITHM_COLORS)] for idx in algo_indices]
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            # Triângulo superior
            self.canvas.create_polygon(x1, y1, x2, y1, cx, cy, fill=colors[0], outline='#95A5A6', width=1)
            # Triângulo inferior esquerdo
            self.canvas.create_polygon(x1, y1, x1, y2, cx, cy, fill=colors[1], outline='#95A5A6', width=1)
            # Triângulo inferior direito
            self.canvas.create_polygon(x2, y2, x1, y2, cx, cy, fill=colors[2], outline='#95A5A6', width=1)
        
        elif num_algos == 4:
            # Dividir em quatro quadrantes
            colors = [self.ALGORITHM_COLORS[idx % len(self.ALGORITHM_COLORS)] for idx in algo_indices]
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            # Quadrante superior esquerdo
            self.canvas.create_rectangle(x1, y1, cx, cy, fill=colors[0], outline='#95A5A6', width=1)
            # Quadrante superior direito
            self.canvas.create_rectangle(cx, y1, x2, cy, fill=colors[1], outline='#95A5A6', width=1)
            # Quadrante inferior esquerdo
            self.canvas.create_rectangle(x1, cy, cx, y2, fill=colors[2], outline='#95A5A6', width=1)
            # Quadrante inferior direito
            self.canvas.create_rectangle(cx, cy, x2, y2, fill=colors[3], outline='#95A5A6', width=1)
        
        else:
            # Para 5+ algoritmos, dividir em setores radiais
            colors = [self.ALGORITHM_COLORS[idx % len(self.ALGORITHM_COLORS)] for idx in algo_indices]
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            angle_step = 360 / num_algos
            
            for i, color in enumerate(colors):
                start_angle = i * angle_step
                self.canvas.create_arc(x1, y1, x2, y2, start=start_angle, extent=angle_step,
                                     fill=color, outline='#95A5A6', width=1, style='pieslice')
    
    def _display_comparison_results(self):
        """Exibe os resultados comparativos de todos os algoritmos."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        text = f"{'='*35}\n"
        text += "COMPARAÇÃO DE ALGORITMOS\n"
        text += f"{'='*35}\n\n"
        
        # Criar tabela de resultados
        for idx, (algo_name, result) in enumerate(self.all_results.items()):
            color_indicator = "■"
            text += f"{color_indicator} {algo_name}:\n"
            
            if result.found:
                text += f"  ✓ Solução encontrada\n"
                text += f"  Profundidade: {result.depth}\n"
                text += f"  Nós Visitados: {result.nodes_visited}\n"
                
                if hasattr(result, 'path_cost') and result.path_cost is not None:
                    text += f"  Custo: {result.path_cost}\n"
                
                text += f"  Tempo: {result.time*1000:.2f}ms\n"
            else:
                text += f"  ✗ Sem solução\n"
            
            text += "\n"
        
        # Adicionar análise comparativa
        text += f"{'='*35}\n"
        text += "ANÁLISE COMPARATIVA\n"
        text += f"{'='*35}\n\n"
        
        successful_results = {name: res for name, res in self.all_results.items() if res.found}
        
        if successful_results:
            # Melhor tempo
            best_time = min(successful_results.items(), key=lambda x: x[1].time)
            text += f"⚡ Mais Rápido: {best_time[0]} ({best_time[1].time*1000:.2f}ms)\n"
            
            # Menor custo
            best_cost = min(successful_results.items(), key=lambda x: x[1].path_cost if hasattr(x[1], 'path_cost') and x[1].path_cost else float('inf'))
            if hasattr(best_cost[1], 'path_cost') and best_cost[1].path_cost:
                text += f"💎 Melhor Custo: {best_cost[0]} (custo: {best_cost[1].path_cost})\n"
            
            # Menos nós visitados
            best_nodes = min(successful_results.items(), key=lambda x: x[1].nodes_visited)
            text += f"🎯 Menos Nós: {best_nodes[0]} ({best_nodes[1].nodes_visited} nós)\n"
        
        self.results_text.insert(tk.END, text)
        self.results_text.config(state=tk.DISABLED)
    
    def _export_results(self):
        """Exporta os resultados de todos os algoritmos para CSV."""
        if not self.all_results:
            messagebox.showerror("Erro", "Nenhum resultado para exportar. Execute a comparação primeiro.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="comparacao_algoritmos.csv"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    
                    # Cabeçalho igual ao all_algorithms_comparison.csv
                    writer.writerow([
                        "maze_id", "algorithm", "heuristic", "path_found", "time_s", 
                        "nodes_visited", "nodes_generated", "max_frontier_size", 
                        "path_cost", "path_length"
                    ])
                    
                    # Dados - maze_id sempre será 1 (labirinto customizado)
                    maze_id = 1
                    
                    for algo_name, result in self.all_results.items():
                        # Separar algoritmo e heurística
                        if "(" in algo_name:
                            # Formato: "Guloso (Manhattan)" ou "A* (Euclidiana)"
                            algo_parts = algo_name.split("(")
                            algorithm = algo_parts[0].strip()
                            heuristic = algo_parts[1].replace(")", "").strip().lower()
                            
                            # Mapear nomes em português para inglês
                            algo_map = {
                                "Guloso": "Greedy",
                                "A*": "A*",
                                "A-Estrela": "A*"
                            }
                            heuristic_map = {
                                "manhattan": "manhattan",
                                "euclidiana": "euclidean",
                                "chebyshev": "chebyshev"
                            }
                            
                            algorithm = algo_map.get(algorithm, algorithm)
                            heuristic = heuristic_map.get(heuristic, heuristic)
                        else:
                            algorithm = algo_name
                            heuristic = "-"
                        
                        # Path length é o tamanho do caminho (depth + 1 para BFS/DFS)
                        path_length = ""
                        if result.found and result.path:
                            path_length = len(result.path)
                        
                        # Nós gerados e fronteira máxima
                        nodes_generated = getattr(result, 'nodes_generated', None)
                        max_frontier = getattr(result, 'max_frontier_size', None)
                        
                        # Path cost
                        path_cost = ""
                        if result.found and hasattr(result, 'path_cost') and result.path_cost is not None:
                            path_cost = result.path_cost
                        
                        writer.writerow([
                            maze_id,
                            algorithm,
                            heuristic,
                            result.found,
                            result.time,
                            result.nodes_visited,
                            nodes_generated if nodes_generated else "-",
                            max_frontier if max_frontier else "-",
                            path_cost,
                            path_length
                        ])
                
                messagebox.showinfo("Sucesso", f"Resultados exportados com sucesso!\n{filename}")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar resultados: {str(e)}")


def main():
    root = tk.Tk()
    app = MazeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
