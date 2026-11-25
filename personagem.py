from dado import Dado


CLASSES_DISPONIVEIS = {
    "Guerreiro": {
        "descricao": "+4 Força | +2 Vitalidade",
        "buffs": {"forca": 4, "defesa": 0, "agilidade": 0, "vitalidade": 2},
    },
    "Mago": {
        "descricao": "+5 Agilidade (Mana) | +2 Força",
        "buffs": {"forca": 2, "defesa": 0, "agilidade": 5, "vitalidade": 0},
    },
    "Paladino": {
        "descricao": "+4 Defesa | +3 Vitalidade",
        "buffs": {"forca": 0, "defesa": 4, "agilidade": 0, "vitalidade": 3},
    },
    "Ladino": {
        "descricao": "+4 Agilidade | +2 Força",
        "buffs": {"forca": 2, "defesa": 0, "agilidade": 4, "vitalidade": 0},
    },
}


class Personagem:
    def __init__(self, nome, classe="Guerreiro"):
        self.nome = nome
        self.classe = classe if classe in CLASSES_DISPONIVEIS else "Guerreiro"

        self.d20 = Dado(20)
        self.d6 = Dado(6)

        buffs = CLASSES_DISPONIVEIS[self.classe]["buffs"]

        self.forca = self._gerar_atributo() + buffs["forca"]
        self.defesa = self._gerar_atributo() + buffs["defesa"]
        self.agilidade = self._gerar_atributo() + buffs["agilidade"]
        self.vitalidade = self._gerar_atributo() + buffs["vitalidade"]

        self.vida_maxima = self.vitalidade * 5
        self.vida = self.vida_maxima

        self.mana_maxima = 20 + (self.agilidade * 2)
        self.mana = self.mana_maxima

        # Dados rolados manualmente pelo jogador na interface
        self.d20_preparado = None
        self.d6_preparado = None

        self.habilidades = {
            "Golpe Poderoso": 8,
            "Bola de Fogo": 12,
            "Ataque Rápido": 6,
            "Cura Mágica": 10,
        }

    def _gerar_atributo(self):
        return 10 + self.d6.rolar()

    def _consumir_d20(self):
        if self.d20_preparado is not None:
            valor = self.d20_preparado
            self.d20_preparado = None
            return valor, True
        return self.d20.rolar(), False

    def _consumir_d6(self):
        if self.d6_preparado is not None:
            valor = self.d6_preparado
            self.d6_preparado = None
            return valor, True
        return self.d6.rolar(), False

    def esta_vivo(self):
        return self.vida > 0

    def tem_mana(self, custo):
        return self.mana >= custo

    def gastar_mana(self, custo):
        if not self.tem_mana(custo):
            return False
        self.mana -= custo
        return True

    def regenerar_mana(self, quantidade=4):
        mana_antes = self.mana
        self.mana = min(self.mana_maxima, self.mana + quantidade)
        return self.mana - mana_antes

    def meditar(self):
        bonus_d6, manual = self._consumir_d6()
        origem = "manual" if manual else "automático"
        total_recuperado = 10 + bonus_d6
        real = self.regenerar_mana(total_recuperado)
        return (
            f"=== {self.nome} ({self.classe}) meditou ===\n"
            f"Rolagem D6 ({origem}): {bonus_d6} + 10 base.\n"
            f"Recuperou {real} de Mana! ({self.mana}/{self.mana_maxima} MP)"
        )

    def atacar(self, adversario):
        dado_ataque, manual_20 = self._consumir_d20()
        dado_defesa = adversario.d20.rolar()

        resultado_ataque = dado_ataque + self.forca
        resultado_defesa = dado_defesa + adversario.defesa
        tag_20 = " [Manual]" if manual_20 else ""

        linhas = [
            f"=== {self.nome} ({self.classe}) atacou {adversario.nome} ===",
            f"{self.nome}: D20({dado_ataque}){tag_20} + Força({self.forca}) = {resultado_ataque}",
            f"{adversario.nome}: D20({dado_defesa}) + Defesa({adversario.defesa}) = {resultado_defesa}",
        ]

        if resultado_ataque >= resultado_defesa:
            modificador, manual_6 = self._consumir_d6()
            tag_6 = " [Manual]" if manual_6 else ""
            dano = self.forca + modificador
            adversario.receber_dano(dano)
            linhas.append(f"Ataque acertou! Dano: Força({self.forca}) + D6({modificador}){tag_6} = {dano}")
            linhas.append(f"Vida de {adversario.nome}: {adversario.vida}/{adversario.vida_maxima}")
        else:
            linhas.append(f"Defesa bem-sucedida! {adversario.nome} bloqueou o golpe.")

        return "\n".join(linhas)

    def usar_habilidade(self, nome_habilidade, adversario):
        if nome_habilidade not in self.habilidades:
            return False, "Habilidade desconhecida."

        custo = self.habilidades[nome_habilidade]
        if not self.gastar_mana(custo):
            return False, f"{self.nome} não tem mana suficiente para {nome_habilidade} (precisa de {custo} MP)."

        if nome_habilidade == "Golpe Poderoso":
            bonus_d6, manual_6 = self._consumir_d6()
            tag_6 = " [Manual]" if manual_6 else ""
            dano = (self.forca * 2) + bonus_d6
            adversario.receber_dano(dano)
            texto = (
                f"=== {self.nome} usou GOLPE PODEROSO (-{custo} MP) ===\n"
                f"D6({bonus_d6}){tag_6} | Dano massivo em {adversario.nome}: {dano}!\n"
                f"Vida de {adversario.nome}: {adversario.vida}/{adversario.vida_maxima}"
            )
            return True, texto

        if nome_habilidade == "Bola de Fogo":
            dado_ataque, manual_20 = self._consumir_d20()
            bonus_d6, manual_6 = self._consumir_d6()
            tag_20 = " [Manual]" if manual_20 else ""
            tag_6 = " [Manual]" if manual_6 else ""

            # Usa Agilidade (afinidade mágica) contra metade da defesa inimiga
            acerto = dado_ataque + self.agilidade
            defesa_magica = adversario.d20.rolar() + (adversario.defesa // 2)

            if acerto >= defesa_magica:
                dano = self.agilidade + (bonus_d6 * 2)
                adversario.receber_dano(dano)
                texto = (
                    f"=== {self.nome} lançou BOLA DE FOGO (-{custo} MP) ===\n"
                    f"Acerto: D20({dado_ataque}){tag_20} + Agilidade({self.agilidade}) = {acerto} vs {defesa_magica}\n"
                    f"Explosão causou {dano} de dano mágico (D6={bonus_d6}{tag_6})!\n"
                    f"Vida de {adversario.nome}: {adversario.vida}/{adversario.vida_maxima}"
                )
            else:
                texto = (
                    f"=== {self.nome} lançou BOLA DE FOGO (-{custo} MP) ===\n"
                    f"Acerto: {acerto} vs Defesa Mágica: {defesa_magica} — {adversario.nome} esquivou das chamas!"
                )
            return True, texto

        if nome_habilidade == "Ataque Rápido":
            dado_ataque, manual_20 = self._consumir_d20()
            bonus_d6, manual_6 = self._consumir_d6()
            tag_20 = " [Manual]" if manual_20 else ""
            tag_6 = " [Manual]" if manual_6 else ""

            acerto = dado_ataque + self.agilidade + 2
            defesa = adversario.d20.rolar() + adversario.defesa

            if acerto >= defesa:
                dano = (self.forca // 2) + (self.agilidade // 2) + bonus_d6
                adversario.receber_dano(dano)
                texto = (
                    f"=== {self.nome} usou ATAQUE RÁPIDO (-{custo} MP) ===\n"
                    f"Acerto veloz: D20({dado_ataque}){tag_20} + Agilidade({self.agilidade}) + 2 = {acerto} vs {defesa}\n"
                    f"Corte preciso causou {dano} de dano (D6={bonus_d6}{tag_6})!\n"
                    f"Vida de {adversario.nome}: {adversario.vida}/{adversario.vida_maxima}"
                )
            else:
                texto = (
                    f"=== {self.nome} usou ATAQUE RÁPIDO (-{custo} MP) ===\n"
                    f"Acerto: {acerto} vs Defesa: {defesa} — O golpe passou raspando!"
                )
            return True, texto

        if nome_habilidade == "Cura Mágica":
            bonus_d6, manual_6 = self._consumir_d6()
            tag_6 = " [Manual]" if manual_6 else ""
            cura = self.vitalidade + bonus_d6
            vida_antes = self.vida
            self.vida = min(self.vida_maxima, self.vida + cura)
            curado_real = self.vida - vida_antes
            texto = (
                f"=== {self.nome} usou CURA MÁGICA (-{custo} MP) ===\n"
                f"D6({bonus_d6}){tag_6} | {self.nome} recuperou {curado_real} de vida! ({self.vida}/{self.vida_maxima})"
            )
            return True, texto

        return False, "Habilidade não implementada."

    def receber_dano(self, dano):
        self.vida -= dano
        if self.vida < 0:
            self.vida = 0
