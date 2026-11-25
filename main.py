import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from datetime import datetime
import traceback
from rpg import RPG


def registrar_erro(exc_type, exc, tb):
    """Registra erros mesmo com pythonw.exe, sem abrir um console."""
    detalhe = ''.join(traceback.format_exception(exc_type, exc, tb))
    arquivo = Path.home() / '.the_battle' / 'erros.log'
    try:
        arquivo.parent.mkdir(parents=True, exist_ok=True)
        with arquivo.open('a', encoding='utf-8') as log:
            log.write(f'\n[{datetime.now().isoformat(timespec="seconds")}] V5.2\n{detalhe}\n')
        local = f'\nDiagnóstico: {arquivo}'
    except OSError:
        local = '\nNão foi possível gravar o diagnóstico.'
    messagebox.showerror('The Battle — erro inesperado', f'{exc_type.__name__}: {exc}{local}')


def main():
    root = tk.Tk()
    root.report_callback_exception = registrar_erro
    try:
        RPG(root)
    except Exception as e:
        registrar_erro(type(e), e, e.__traceback__)
        root.destroy()
        return
    root.mainloop()


if __name__ == '__main__':
    main()
