import random

class GeradorNota:
    @staticmethod
    def gerar_nota():
        return round(random.uniform(0, 10), 2)

    @staticmethod
    def gerar_faltas():
        return random.randint(0, 15)
