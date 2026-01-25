# src/config.py
import os
import sys
from pathlib import Path

# ==============================================================================
# 1. Definição de Diretórios (Compatível com PyInstaller/Executável)
# ==============================================================================
if getattr(sys, 'frozen', False):
    # Se estiver rodando como .exe
    ROOT_DIR = Path(sys.executable).parent
else:
    # Se estiver rodando como script Python normal
    # Assume que este arquivo está em /src, então volta uma pasta para a raiz
    ROOT_DIR = Path(__file__).parent.parent

DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = ROOT_DIR / "outputs"
ASSETS_DIR = ROOT_DIR / "assets"

# Banco de dados
DB_NAME = "canopy_runs.db"
DB_PATH = ROOT_DIR / DB_NAME

# ==============================================================================
# 2. Configurações da Interface Gráfica (GUI)
# ==============================================================================
APP_NAME = "PryAI Canopy"
APP_VERSION = "2.0.0 (Open Source)"
WINDOW_SIZE = "1100x700"

# Cores e Temas (CustomTkinter)
APPEARANCE_MODE = "System"  # "System" (segue o OS), "Dark", "Light"
COLOR_THEME = "green"   # "blue", "green", "dark-blue"

# ==============================================================================
# 3. Inicialização
# ==============================================================================
def init_directories():
    """Cria as pastas necessárias se elas não existirem."""
    for folder in [DATA_DIR, OUTPUT_DIR, ASSETS_DIR]:
        folder.mkdir(parents=True, exist_ok=True)