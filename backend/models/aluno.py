class Aluno:
    def __init__(self, aluno_id, nome, email, curso, status, turma, sexo, idade, trabalha, renda_familiar, acompanhamento_medico, tem_filho, estado_civil, semestre, bimestre):
        self.aluno_id = aluno_id
        self.nome = nome
        self.email = email
        self.curso = curso
        self.status = status
        self.turma = turma
        self.sexo = sexo
        self.idade = idade
        self.trabalha = trabalha
        self.renda_familiar = renda_familiar
        self.acompanhamento_medico = acompanhamento_medico
        self.tem_filho = tem_filho
        self.estado_civil = estado_civil
        self.semestre = semestre
        self.bimestre = bimestre
        self.disciplinas = []
        self.professores = []
        self.notas = []
        self.faltas = []
        self.desempenhos = []
        self.risco_evasao = 0

    def to_dict(self):
        base = {
            'aluno_id': self.aluno_id,
            'nome_aluno': self.nome,
            'email_aluno': self.email,
            'curso': self.curso,
            'status': self.status,
            'turma': self.turma,
            'sexo': self.sexo,
            'idade': self.idade,
            'trabalha': self.trabalha,
            'renda_familiar': self.renda_familiar,
            'acompanhamento_medico': self.acompanhamento_medico,
            'tem_filho': self.tem_filho,
            'estado_civil': self.estado_civil,
            'semestre': self.semestre,
            'bimestre': self.bimestre
        }

        for i in range(5):
            base[f'aula_{i + 1}'] = self.disciplinas[i]
            base[f'professor_{i + 1}'] = self.professores[i]
            base[f'notas_{i + 1}'] = self.notas[i]
            base[f'faltas_{i + 1}'] = self.faltas[i]
            base[f'desempenho_{i + 1}'] = self.desempenhos[i]

        base['risco_evasao'] = self.risco_evasao
        return base
