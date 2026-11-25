import tkinter as tk
from tkinter import messagebox, ttk
from personagem import Personagem, CLASSES_DISPONIVEIS


class MedievalBattleGUI:
    BG_FUNDO = "#1B1612"
    BG_CARD = "#2A211B"
    BG_LOG = "#120E0B"
    BG_INPUT = "#F4EBD9"
    FG_TITULO = "#F5C451"
    FG_TEXTO = "#F3E9D2"
    FG_MUTED = "#C7B89E"
    BORDA_CARD = "#5C4328"

    def __init__(self, root):
        self.root = root
        self.root.title("The Battle")
        self.root.geometry("860x700")
        self.root.configure(bg=self.BG_FUNDO)

        self._configurar_estilos()

        self.p1 = None
        self.p2 = None
        self.turno = 1
        self.jogador_atual = None
        self.alvo_atual = None
        self._construir_tela_criacao()

    def _configurar_estilos(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")

        base_cfg = {
            "troughcolor": "#3B2E24",
            "bordercolor": "#5C4328",
            "lightcolor": "#5C4328",
            "darkcolor": "#241B15",
            "thickness": 18,
        }
        style.configure("HP.Alta.Horizontal.TProgressbar", background="#2E7D32", **base_cfg)
        style.configure("HP.Media.Horizontal.TProgressbar", background="#EF6C00", **base_cfg)
        style.configure("HP.Baixa.Horizontal.TProgressbar", background="#C62828", **base_cfg)

    def _limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def _construir_tela_criacao(self):
        self._limpar_tela()
        self.root.configure(bg=self.BG_FUNDO)

        tk.Label(
            self.root,
            text="⚔️ The Battle ⚔️",
            bg=self.BG_FUNDO,
            fg=self.FG_TITULO,
            font=("System", 24, "bold"),
        ).pack(pady=(20, 8))

        intro = (
            "Escolha os nomes e as classes dos combatentes.\n"
            "• Role o D20 para liberar: Ataque Básico, Bola de Fogo e Ataque Rápido.\n"
            "• Role o D6 para liberar: Meditar (Mana), Golpe Poderoso, Cura Mágica (ou somar dano aos ataques)."
        )
        tk.Label(
            self.root,
            text=intro,
            bg=self.BG_FUNDO,
            fg=self.FG_TEXTO,
            font=("Segoe UI", 10),
            justify="center",
        ).pack(pady=6)

        frame_form = tk.Frame(
            self.root,
            bg=self.BG_CARD,
            highlightbackground=self.BORDA_CARD,
            highlightthickness=2,
            padx=22,
            pady=18,
        )
        frame_form.pack(pady=14)

        lista_classes = list(CLASSES_DISPONIVEIS.keys())

        tk.Label(
            frame_form,
            text="Nome do Personagem 1:",
            bg=self.BG_CARD,
            fg=self.FG_TEXTO,
            font=("Segoe UI", 11, "bold"),
        ).grid(row=0, column=0, padx=10, pady=8, sticky="e")

        self.entry_p1 = tk.Entry(
            frame_form,
            font=("Segoe UI", 11),
            width=22,
            bg=self.BG_INPUT,
            fg="#1B1612",
        )
        self.entry_p1.insert(0, "Player 1")
        self.entry_p1.grid(row=0, column=1, padx=10, pady=8)

        tk.Label(
            frame_form,
            text="Classe P1:",
            bg=self.BG_CARD,
            fg=self.FG_TEXTO,
            font=("Segoe UI", 11, "bold"),
        ).grid(row=1, column=0, padx=10, pady=8, sticky="e")

        self.combo_classe_p1 = ttk.Combobox(
            frame_form, values=lista_classes, state="readonly", font=("Segoe UI", 11), width=20
        )
        self.combo_classe_p1.set("Guerreiro")
        self.combo_classe_p1.grid(row=1, column=1, padx=10, pady=8)

        self.lbl_buff_p1 = tk.Label(
            frame_form,
            text=CLASSES_DISPONIVEIS["Guerreiro"]["descricao"],
            bg=self.BG_CARD,
            fg=self.FG_TITULO,
            font=("Segoe UI", 9, "italic"),
        )
        self.lbl_buff_p1.grid(row=1, column=2, padx=10, pady=8, sticky="w")
        self.combo_classe_p1.bind(
            "<<ComboboxSelected>>",
            lambda e: self.lbl_buff_p1.config(text=CLASSES_DISPONIVEIS[self.combo_classe_p1.get()]["descricao"]),
        )

        ttk.Separator(frame_form, orient="horizontal").grid(row=2, column=0, columnspan=3, sticky="ew", pady=10)

        tk.Label(
            frame_form,
            text="Nome do Personagem 2:",
            bg=self.BG_CARD,
            fg=self.FG_TEXTO,
            font=("Segoe UI", 11, "bold"),
        ).grid(row=3, column=0, padx=10, pady=8, sticky="e")

        self.entry_p2 = tk.Entry(
            frame_form,
            font=("Segoe UI", 11),
            width=22,
            bg=self.BG_INPUT,
            fg="#1B1612",
        )
        self.entry_p2.insert(0, "Player 2")
        self.entry_p2.grid(row=3, column=1, padx=10, pady=8)

        tk.Label(
            frame_form,
            text="Classe P2:",
            bg=self.BG_CARD,
            fg=self.FG_TEXTO,
            font=("Segoe UI", 11, "bold"),
        ).grid(row=4, column=0, padx=10, pady=8, sticky="e")

        self.combo_classe_p2 = ttk.Combobox(
            frame_form, values=lista_classes, state="readonly", font=("Segoe UI", 11), width=20
        )
        self.combo_classe_p2.set("Mago")
        self.combo_classe_p2.grid(row=4, column=1, padx=10, pady=8)

        self.lbl_buff_p2 = tk.Label(
            frame_form,
            text=CLASSES_DISPONIVEIS["Mago"]["descricao"],
            bg=self.BG_CARD,
            fg=self.FG_TITULO,
            font=("Segoe UI", 9, "italic"),
        )
        self.lbl_buff_p2.grid(row=4, column=2, padx=10, pady=8, sticky="w")
        self.combo_classe_p2.bind(
            "<<ComboboxSelected>>",
            lambda e: self.lbl_buff_p2.config(text=CLASSES_DISPONIVEIS[self.combo_classe_p2.get()]["descricao"]),
        )

        tk.Button(
            self.root,
            text="Iniciar Combate",
            font=("Segoe UI", 12, "bold"),
            bg="#2E7D32",
            activebackground="#388E3C",
            fg="white",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=24,
            pady=10,
            command=self._iniciar_combate,
        ).pack(pady=14)

    def _iniciar_combate(self):
        nome1 = self.entry_p1.get().strip() or "Personagem 1"
        classe1 = self.combo_classe_p1.get()

        nome2 = self.entry_p2.get().strip() or "Personagem 2"
        classe2 = self.combo_classe_p2.get()

        self.p1 = Personagem(nome1, classe1)
        self.p2 = Personagem(nome2, classe2)
        self.turno = 1
        self.jogador_atual = self.p1
        self.alvo_atual = self.p2

        self._construir_tela_combate()
        self._comecar_turno_jogador()

    def _criar_card_personagem(self, parent, titulo_inicial, side):
        card = tk.LabelFrame(
            parent,
            text=titulo_inicial,
            bg=self.BG_CARD,
            fg=self.FG_TITULO,
            font=("Georgia", 12, "bold"),
            highlightbackground=self.BORDA_CARD,
            highlightthickness=2,
            padx=14,
            pady=10,
        )
        card.pack(side=side, expand=True, fill="both", padx=(0, 10) if side == "left" else (10, 0))

        linha_hp = tk.Frame(card, bg=self.BG_CARD)
        linha_hp.pack(fill="x", pady=(2, 4))

        tk.Label(
            linha_hp,
            text="HP",
            bg=self.BG_CARD,
            fg="#FF6B6B",
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left")

        lbl_hp = tk.Label(
            linha_hp,
            text="",
            bg=self.BG_CARD,
            fg=self.FG_TEXTO,
            font=("Segoe UI", 10, "bold"),
        )
        lbl_hp.pack(side="right")

        barra_hp = ttk.Progressbar(
            card,
            orient="horizontal",
            mode="determinate",
            style="HP.Alta.Horizontal.TProgressbar",
        )
        barra_hp.pack(fill="x", pady=(0, 8))

        lbl_stats = tk.Label(
            card,
            text="",
            font=("Segoe UI", 10),
            bg=self.BG_CARD,
            fg=self.FG_TEXTO,
            justify="left",
        )
        lbl_stats.pack(anchor="w")

        return card, lbl_hp, barra_hp, lbl_stats

    def _construir_tela_combate(self):
        self._limpar_tela()
        self.root.configure(bg=self.BG_FUNDO)

        self.lbl_turno = tk.Label(
            self.root,
            text="",
            bg=self.BG_FUNDO,
            fg=self.FG_TITULO,
            font=("Georgia", 15, "bold"),
        )
        self.lbl_turno.pack(pady=(10, 6))

        frame_status = tk.Frame(self.root, bg=self.BG_FUNDO)
        frame_status.pack(fill="x", padx=20)

        self.card_p1, self.lbl_hp_p1, self.barra_hp_p1, self.lbl_status_p1 = self._criar_card_personagem(
            frame_status, "Personagem 1", "left"
        )
        self.card_p2, self.lbl_hp_p2, self.barra_hp_p2, self.lbl_status_p2 = self._criar_card_personagem(
            frame_status, "Personagem 2", "right"
        )

        # Painel de Rolagem de Dados Vinculada
        frame_dados = tk.LabelFrame(
            self.root,
            text="🎲 Passo 1: Role o dado necessário para liberar sua ação",
            bg=self.BG_CARD,
            fg=self.FG_TITULO,
            font=("Segoe UI", 10, "bold"),
            highlightbackground=self.BORDA_CARD,
            highlightthickness=1,
            padx=12,
            pady=8,
        )
        frame_dados.pack(fill="x", padx=20, pady=(10, 4))

        self.btn_rolar_d20 = tk.Button(
            frame_dados,
            text="🎲 Rolar D20 (Libera Ataques)",
            font=("Segoe UI", 10, "bold"),
            bg="#5E35B1",
            activebackground="#673AB7",
            fg="white",
            disabledforeground="#B0BEC5",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=5,
            command=self._rolar_d20_manual,
        )
        self.btn_rolar_d20.pack(side="left", padx=(0, 8))
        self.lbl_d20_atual = tk.Label(
            frame_dados,
            text="D20: Aguardando",
            bg=self.BG_CARD,
            fg=self.FG_MUTED,
            font=("Segoe UI", 10, "bold"),
        )
        self.lbl_d20_atual.pack(side="left", padx=(0, 24))

        self.btn_rolar_d6 = tk.Button(
            frame_dados,
            text="🎲 Rolar D6 (Libera Mana/Cura/Poder)",
            font=("Segoe UI", 10, "bold"),
            bg="#5E35B1",
            activebackground="#673AB7",
            fg="white",
            disabledforeground="#B0BEC5",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=5,
            command=self._rolar_d6_manual,
        )
        self.btn_rolar_d6.pack(side="left", padx=(0, 8))

        self.lbl_d6_atual = tk.Label(
            frame_dados,
            text="D6: Aguardando",
            bg=self.BG_CARD,
            fg=self.FG_MUTED,
            font=("Segoe UI", 10, "bold"),
        )
        self.lbl_d6_atual.pack(side="left")

        # Painel de Ações em 2 linhas (Linha 0 = D20 | Linha 1 = D6)
        frame_acoes = tk.Frame(self.root, bg=self.BG_FUNDO)
        frame_acoes.pack(pady=8)

        estilo_btn = {
            "font": ("Segoe UI", 10, "bold"),
            "fg": "white",
            "activeforeground": "white",
            "disabledforeground": "#78909C",
            "relief": "flat",
            "cursor": "hand2",
            "padx": 10,
            "pady": 6,
            "width": 25,
        }

        # Linha 0: Exigem D20
        self.btn_atacar = tk.Button(
            frame_acoes,
            text="⚔️ Ataque Básico [Requer D20]",
            bg="#1565C0",
            activebackground="#1976D2",
            command=self._acao_ataque_basico,
            **estilo_btn,
        )
        self.btn_atacar.grid(row=0, column=0, padx=5, pady=4)

        self.btn_fogo = tk.Button(
            frame_acoes,
            text="🔥 Bola de Fogo (12 MP) [D20]",
            bg="#C62828",
            activebackground="#D32F2F",
            command=lambda: self._acao_habilidade("Bola de Fogo"),
            **estilo_btn,
        )
        self.btn_fogo.grid(row=0, column=1, padx=5, pady=4)

        self.btn_rapido = tk.Button(
            frame_acoes,
            text="⚡ Ataque Rápido (6 MP) [D20]",
            bg="#AD1457",
            activebackground="#C2185B",
            command=lambda: self._acao_habilidade("Ataque Rápido"),
            **estilo_btn,
        )
        self.btn_rapido.grid(row=0, column=2, padx=5, pady=4)

        # Linha 1: Exigem D6
        self.btn_meditar = tk.Button(
            frame_acoes,
            text="🧘 Recarregar Mana [Requer D6]",
            bg="#2E7D32",
            activebackground="#388E3C",
            command=self._acao_meditar,
            **estilo_btn,
        )
        self.btn_meditar.grid(row=1, column=0, padx=5, pady=4)

        self.btn_golpe = tk.Button(
            frame_acoes,
            text="💥 Golpe Poderoso (8 MP) [D6]",
            bg="#EF6C00",
            activebackground="#F57C00",
            command=lambda: self._acao_habilidade("Golpe Poderoso"),
            **estilo_btn,
        )
        self.btn_golpe.grid(row=1, column=1, padx=5, pady=4)

        self.btn_cura = tk.Button(
            frame_acoes,
            text="✨ Cura Mágica (10 MP) [D6]",
            bg="#00897B",
            activebackground="#009688",
            command=lambda: self._acao_habilidade("Cura Mágica"),
            **estilo_btn,
        )
        self.btn_cura.grid(row=1, column=2, padx=5, pady=4)

        tk.Label(
            self.root,
            bg=self.BG_FUNDO,
            fg=self.FG_MUTED,
            text="📜 Registro de Combate:",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", padx=20)

        self.txt_log = tk.Text(
            self.root,
            height=10,
            font=("Segoe UI", 10),
            bg=self.BG_LOG,
            fg=self.FG_TEXTO,
            insertbackground=self.FG_TEXTO,
            highlightbackground=self.BORDA_CARD,
            highlightthickness=1,
            relief="flat",
            state="disabled",
            wrap="word",
        )
        self.txt_log.pack(fill="both", expand=True, padx=20, pady=(4, 14))

        self._atualizar_status()

    def _rolar_d20_manual(self):
        if self.jogador_atual.d20_preparado is not None:
            return
        valor = self.jogador_atual.d20.rolar()
        self.jogador_atual.d20_preparado = valor
        self._log(f"🎲 {self.jogador_atual.nome} rolou o D20 e tirou: {valor}! (Ataques liberados)")
        self._atualizar_status()

    def _rolar_d6_manual(self):
        if self.jogador_atual.d6_preparado is not None:
            return
        valor = self.jogador_atual.d6.rolar()
        self.jogador_atual.d6_preparado = valor
        self._log(f"🎲 {self.jogador_atual.nome} rolou o D6 e tirou: {valor}! (Recarga de Mana, Golpe Poderoso e Cura liberados)")
        self._atualizar_status()

    def _log(self, mensagem):
        self.txt_log.config(state="normal")
        self.txt_log.insert("end", mensagem + "\n\n")
        self.txt_log.see("end")
        self.txt_log.config(state="disabled")

    def _formatar_status(self, p):
        return (
            f"Classe: {p.classe} | Mana: {p.mana} / {p.mana_maxima}\n"
            f"Força: {p.forca} | Defesa: {p.defesa}\n"
            f"Agilidade: {p.agilidade} | Vitalidade: {p.vitalidade}"
        )

    def _atualizar_barra_hp(self, p, lbl_hp, barra_hp):
        vida_atual = max(0, min(p.vida, p.vida_maxima))
        barra_hp["maximum"] = max(1, p.vida_maxima)
        barra_hp["value"] = vida_atual
        lbl_hp.config(text=f"{vida_atual} / {p.vida_maxima}")

        percentual = vida_atual / max(1, p.vida_maxima)
        if percentual > 0.5:
            estilo = "HP.Alta.Horizontal.TProgressbar"
        elif percentual > 0.25:
            estilo = "HP.Media.Horizontal.TProgressbar"
        else:
            estilo = "HP.Baixa.Horizontal.TProgressbar"
        barra_hp.config(style=estilo)

    def _atualizar_status(self):
        self.card_p1.config(text=f"{self.p1.nome} ({self.p1.classe})")
        self.card_p2.config(text=f"{self.p2.nome} ({self.p2.classe})")

        self._atualizar_barra_hp(self.p1, self.lbl_hp_p1, self.barra_hp_p1)
        self._atualizar_barra_hp(self.p2, self.lbl_hp_p2, self.barra_hp_p2)

        self.lbl_status_p1.config(text=self._formatar_status(self.p1))
        self.lbl_status_p2.config(text=self._formatar_status(self.p2))
        self.lbl_turno.config(text=f"TURNO {self.turno} — Vez de: {self.jogador_atual.nome}")

        self.card_p1.config(highlightbackground=self.FG_TITULO if self.jogador_atual is self.p1 else self.BORDA_CARD)
        self.card_p2.config(highlightbackground=self.FG_TITULO if self.jogador_atual is self.p2 else self.BORDA_CARD)

        d20_prep = self.jogador_atual.d20_preparado
        d6_prep = self.jogador_atual.d6_preparado

        tem_d20 = d20_prep is not None
        tem_d6 = d6_prep is not None

        self.lbl_d20_atual.config(
            text=f"D20: {d20_prep} (Pronto!)" if tem_d20 else "D20: Aguardando",
            fg=self.FG_TITULO if tem_d20 else self.FG_MUTED,
        )
        self.lbl_d6_atual.config(
            text=f"D6: {d6_prep} (Pronto!)" if tem_d6 else "D6: Aguardando",
            fg=self.FG_TITULO if tem_d6 else self.FG_MUTED,
        )

        # Cada dado pode ser rolado 1 vez por turno de forma independente
        self.btn_rolar_d20.config(state="normal" if not tem_d20 else "disabled")
        self.btn_rolar_d6.config(state="normal" if not tem_d6 else "disabled")

        # Ações vinculadas ao D20
        self.btn_atacar.config(state="normal" if tem_d20 else "disabled")
        self.btn_fogo.config(state="normal" if (tem_d20 and self.jogador_atual.tem_mana(12)) else "disabled")
        self.btn_rapido.config(state="normal" if (tem_d20 and self.jogador_atual.tem_mana(6)) else "disabled")

        # Ações vinculadas ao D6
        self.btn_meditar.config(state="normal" if tem_d6 else "disabled")
        self.btn_golpe.config(state="normal" if (tem_d6 and self.jogador_atual.tem_mana(8)) else "disabled")
        self.btn_cura.config(state="normal" if (tem_d6 and self.jogador_atual.tem_mana(10)) else "disabled")

    def _comecar_turno_jogador(self):
        regen = self.jogador_atual.regenerar_mana(4)
        if regen > 0:
            self._log(f"{self.jogador_atual.nome} regenerou {regen} de mana no início do turno.")
        self._atualizar_status()

    def _acao_ataque_basico(self):
        resultado = self.jogador_atual.atacar(self.alvo_atual)
        self._log(resultado)
        self._finalizar_acao_turno()

    def _acao_habilidade(self, nome_habilidade):
        sucesso, resultado = self.jogador_atual.usar_habilidade(nome_habilidade, self.alvo_atual)
        self._log(resultado)
        if not sucesso:
            messagebox.showwarning("Sem Mana", resultado)
            return
        self._finalizar_acao_turno()

    def _acao_meditar(self):
        resultado = self.jogador_atual.meditar()
        self._log(resultado)
        self._finalizar_acao_turno()

    def _finalizar_acao_turno(self):
        self.jogador_atual.d20_preparado = None
        self.jogador_atual.d6_preparado = None

        self._atualizar_status()

        if not self.alvo_atual.esta_vivo():
            vencedor = self.jogador_atual.nome
            self._log(f"FIM DE JOGO! {vencedor} venceu!")
            self._bloquear_botoes()
            resposta = messagebox.askyesno("Fim de Jogo", f"{vencedor} venceu!\nDeseja jogar novamente?")
            if resposta:
                self._construir_tela_criacao()
            return

        if self.jogador_atual is self.p1:
            self.jogador_atual = self.p2
            self.alvo_atual = self.p1
        else:
            self.jogador_atual = self.p1
            self.alvo_atual = self.p2
            self.turno += 1
        self._comecar_turno_jogador()
    def _bloquear_botoes(self):
        for btn in (
        self.btn_atacar,
        self.btn_golpe,
        self.btn_fogo,
        self.btn_rapido,
        self.btn_cura,
        self.btn_meditar,
        self.btn_rolar_d20,
        self.btn_rolar_d6,
        ):btn.config(state="disabled")