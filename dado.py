import random


class Dado:
    def __init__(self, lados):
        if lados < 2:
            raise ValueError("O dado precisa ter pelo menos 2 lados")
        self.lados = lados

    def rolar(self):
        return random.randint(1, self.lados)

    def __str__(self):
        return f"D{self.lados}"
        