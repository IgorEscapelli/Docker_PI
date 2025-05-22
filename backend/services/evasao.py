class CalculadoraRiscoEvasao:
    @staticmethod
    def calcular(aluno):
        risco = 0
        if aluno.renda_familiar < 2000:
            risco += 1
        if aluno.trabalha == 1:
            risco += 1
        if aluno.tem_filho == 1:
            risco += 1
        if aluno.estado_civil not in ['Solteiro(a)', 'Relacionado(a)']:
            risco += 1
        if aluno.acompanhamento_medico == 1:
            risco += 1
        if aluno.idade > 30:
            risco += 1

        desempenho_ruim = sum(1 for d in aluno.desempenhos if d in ['Ruim', 'Regular'])
        if desempenho_ruim >= 3:
            risco += 1

        return 1 if risco >= 4 else 0
