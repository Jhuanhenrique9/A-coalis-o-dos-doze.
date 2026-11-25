"""Regressão da criação de campanha com widgets reais (Tkinter).
Linux sem monitor: xvfb-run -a -s '-screen 0 1366x768x24' python -m unittest -v test_interface_gui
Windows: python -m unittest -v test_interface_gui
Os testes usam salvamentos temporários, nunca o progresso real do usuário.
"""
import tempfile
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from unittest import TestCase, mock, SkipTest
import rpg
from reliquias import Campanha
from personagem import CLASSES_DISPONIVEIS
from mundo import DISTRITOS


class CriacaoGUI(TestCase):
    def contexto(self, patch):
        valor = patch.start()
        self.addCleanup(patch.stop)
        return valor

    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as e:
            raise SkipTest(f'Tkinter sem monitor: {e}')
        self.addCleanup(self.root.destroy)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.save = Path(self.tmp.name) / 'campanha.json'
        salvar, carregar = Campanha.salvar, Campanha.carregar
        self.contexto(mock.patch.object(rpg, 'SAVE', self.save))
        self.contexto(mock.patch.object(Campanha, 'salvar', lambda obj: salvar(obj, self.save)))
        self.contexto(mock.patch.object(Campanha, 'carregar', classmethod(lambda cls: carregar(self.save))))
        self.contexto(mock.patch.object(rpg, 'Audio'))
        self.contexto(mock.patch.object(rpg.messagebox, 'askyesno', return_value=True))
        self.erros = self.contexto(mock.patch.object(rpg.messagebox, 'showerror'))
        self.falhas = []
        self.root.report_callback_exception = lambda *args: self.falhas.append(args[1])
        self.app = rpg.RPG(self.root)
        self.addCleanup(self.app.cancelar_transicoes)
        self.root.update()

    def widgets(self, parent=None):
        for child in (parent or self.root).winfo_children():
            yield child
            yield from self.widgets(child)

    def botao(self, inicio):
        return next(w for w in self.widgets() if isinstance(w, tk.Button) and w.cget('text').startswith(inicio))

    def visivel(self, w):
        self.assertTrue(w.winfo_ismapped(), w.cget('text'))
        x, y = w.winfo_rootx(), w.winfo_rooty()
        self.assertGreaterEqual(x, self.root.winfo_rootx())
        self.assertGreaterEqual(y, self.root.winfo_rooty())
        self.assertLessEqual(x+w.winfo_width(), min(self.root.winfo_screenwidth(), self.root.winfo_rootx()+self.root.winfo_width()))
        self.assertLessEqual(y+w.winfo_height(), min(self.root.winfo_screenheight(), self.root.winfo_rooty()+self.root.winfo_height()))

    def clicar(self, inicio):
        b = self.botao(inicio)
        self.visivel(b)
        self.assertNotEqual(b.cget('state'), 'disabled')
        b.invoke()
        self.root.update()
        self.assertFalse(self.falhas, self.falhas)

    def test_48_combinacoes_e_prologo(self):
        opcoes = ('Assinar uma denúncia', 'Manter Ione', 'Examinar o astrolábio')
        chaves = ('testemunhar', 'sigilo', 'investigar')
        for i, classe in enumerate(CLASSES_DISPONIVEIS):
            for j, distrito in enumerate(DISTRITOS):
                with self.subTest(classe=classe, distrito=distrito.signo):
                    self.clicar('Nova campanha')
                    c, d = [w for w in self.widgets() if isinstance(w, ttk.Combobox)]
                    c.set(classe); d.current(j)
                    d.event_generate('<<ComboboxSelected>>'); self.root.update()
                    self.clicar('Começar a história')
                    self.assertEqual(self.app.c.p.classe, classe)
                    self.assertEqual(self.app.c.origem, distrito.signo)
                    for op in opcoes: self.visivel(self.botao(op))
                    self.clicar(opcoes[(i+j)%3])
                    self.assertEqual(self.app.c.prologo, chaves[(i+j)%3])
                    self.assertEqual(self.app.c.xp, 15)
                    self.assertIsNotNone(self.botao('[Masmorra'))
                    self.clicar('Menu'); self.clicar('Continuar campanha')
                    self.assertEqual(self.app.c.prologo, chaves[(i+j)%3])
                    self.assertEqual(self.app.c.origem, distrito.signo)
                    self.clicar('Menu')
        self.erros.assert_not_called()

    def test_retomar_prologo_e_janela_minima(self):
        self.root.geometry(f'{self.root.minsize()[0]}x{self.root.minsize()[1]}+8+8'); self.root.update()
        self.clicar('Nova campanha'); self.clicar('Começar a história')
        self.clicar('Menu'); self.clicar('Continuar campanha')
        self.assertIsNone(self.app.c.prologo)
        self.clicar('Manter Ione')
        self.assertEqual(self.app.c.ouro, 28)
        self.erros.assert_not_called()

    def test_falha_de_gravacao_nao_descarta_campanha(self):
        self.clicar('Nova campanha'); self.clicar('Começar a história'); self.clicar('Assinar uma denúncia'); self.clicar('Menu')
        anterior = self.app.c
        self.clicar('Nova campanha')
        with mock.patch.object(Campanha, 'salvar', side_effect=PermissionError('Sem permissão')):
            self.clicar('Começar a história')
        self.assertIs(self.app.c, anterior)
        self.assertTrue(self.save.exists())
        self.erros.assert_called_once()
        self.clicar('Começar a história'); self.clicar('Examinar o astrolábio')
        self.assertEqual(self.app.c.prologo, 'investigar')
