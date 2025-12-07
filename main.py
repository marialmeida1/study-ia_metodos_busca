# main.py
# Interface gráfica interativa para criar e resolver labirintos com algoritmos de busca.

import tkinter as tk
from maze_gui import MazeGUI


def main():
    """Inicia a interface gráfica do solver de labirintos."""
    print("Iniciando Interface Gráfica do Solver de Labirintos...")
    print("Crie labirintos customizados e teste algoritmos de busca!")
    print("=" * 60)
    
    try:
        root = tk.Tk()
        app = MazeGUI(root)
        root.mainloop()
    except ImportError as e:
        print(f"❌ Erro: {e}")
        print("💡 Certifique-se de que o tkinter está instalado.")
    except Exception as e:
        print(f"❌ Erro ao iniciar a GUI: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()