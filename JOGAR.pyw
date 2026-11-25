"""Inicializador alternativo sem console no Windows."""
from pathlib import Path
import os
import runpy
import sys

if __name__ == "__main__":
    pasta = Path(__file__).resolve().parent
    os.chdir(pasta)
    sys.path.insert(0, str(pasta))
    runpy.run_path(str(pasta / "main.py"), run_name="__main__")
