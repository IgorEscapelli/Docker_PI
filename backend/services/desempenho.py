class CalculadoraDesempenho:
    @staticmethod
    def avaliar(nota, faltas):
        if nota >= 8 and faltas <= 3:
            return 'Excelente'
        elif nota >= 7 and faltas <= 5:
            return 'Bom'
        elif nota >= 5 and faltas <= 10:
            return 'Regular'
        else:
            return 'Ruim'
