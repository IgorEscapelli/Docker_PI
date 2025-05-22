import random

class GeradorGrade:
    def __init__(self, disciplinas_por_curso, professores, disciplinas_gerais):
        self.disciplinas_por_curso = disciplinas_por_curso
        self.professores = professores
        self.disciplinas_gerais = disciplinas_gerais
        self.cache = {}

    def obter_grade(self, turma, semestre, bimestre, curso):
        chave = (turma, semestre, bimestre)
        if chave not in self.cache:
            disciplinas = self.disciplinas_por_curso.get(curso, self.disciplinas_gerais)
            escolhidas = random.sample(disciplinas, 5)
            professores = random.sample(self.professores, 5)
            self.cache[chave] = list(zip(escolhidas, professores))
        return self.cache[chave]
