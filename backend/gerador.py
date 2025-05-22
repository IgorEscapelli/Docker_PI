from faker import Faker
import random

from models.aluno import Aluno
from services.desempenho import CalculadoraDesempenho
from services.evasao import CalculadoraRiscoEvasao
from services.erro_injector import ErroInjector
from services.grade_generator import GeradorGrade
from services.nota import GeradorNota
from utils.exportador import ExportadorCSV
import pandas as pd
from sqlalchemy import create_engine

# Configuração do banco
usuario = 'dbpi'
senha = 'walker1207'
host = 'db'
porta = '3306'
nome_banco = 'faculdades1'
tabela_destino = 'alunos'

# Criar engine de conexão
engine = create_engine(f'mysql+pymysql://{usuario}:{senha}@{host}:{porta}/{nome_banco}')

from utils.disciplinas import disciplinas_por_curso, disciplinas_gerais

faker = Faker('pt_BR')

num_alunos = 10000 #Altera a quantidade de dados que serão gerados
cursos = list(disciplinas_por_curso.keys())
status_list = ['Matriculado', 'Trancado', 'Cancelado', 'Concluso']
turmas = ['A', 'B', 'C', 'D']
sexos = ['Masculino', 'Feminino', 'Outro']
estado_civil_list = ['Solteiro(a)', 'Casado(a)','Amasiado(a)','Separado(a)','Divorciado(a)', 'Viúvo(a)']
professores = [faker.name() for _ in range(10000)]

gerador_grade = GeradorGrade(disciplinas_por_curso, professores, disciplinas_gerais)
alunos = []

for aluno_id in range(1, num_alunos + 1):
    aluno = Aluno(
        aluno_id=aluno_id,
        nome=faker.name(),
        email=faker.email(),
        curso=random.choice(cursos),
        status=random.choice(status_list),
        turma=random.choice(turmas),
        sexo=random.choice(sexos),
        idade=random.randint(17, 70),
        trabalha=random.choice([0, 1]),
        renda_familiar=random.randint(800, 10000),
        acompanhamento_medico=random.choice([0, 1]),
        tem_filho=random.choice([0, 1]),
        estado_civil=random.choice(estado_civil_list),
        semestre=random.randint(1, 8),
        bimestre=random.randint(1, 4)
    )

    grade = gerador_grade.obter_grade(aluno.turma, aluno.semestre, aluno.bimestre, aluno.curso)

    for aula, professor in grade:
        nota = GeradorNota.gerar_nota()
        faltas = GeradorNota.gerar_faltas()
        desempenho = CalculadoraDesempenho.avaliar(nota, faltas)

        aluno.disciplinas.append(aula)
        aluno.professores.append(professor)
        aluno.notas.append(nota)
        aluno.faltas.append(faltas)
        aluno.desempenhos.append(desempenho)

    aluno.risco_evasao = CalculadoraRiscoEvasao.calcular(aluno)

    aluno_dict = aluno.to_dict()
    aluno_dict = ErroInjector.aplicar(aluno_dict)
    for key, value in aluno_dict.items():
        if hasattr(aluno, key):
            setattr(aluno, key, value)

    alunos.append(aluno)

ExportadorCSV.exportar(alunos, 'alunos_com_erros.csv')

# Criar e inserir no BD
dados = [aluno.to_dict() for aluno in alunos]
df = pd.DataFrame(dados)
df.to_sql(tabela_destino, con=engine, index=False, if_exists='replace')
print(f"{num_alunos} alunos inseridos na tabela '{tabela_destino}' do banco '{nome_banco}'!")