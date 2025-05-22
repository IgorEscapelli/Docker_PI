CREATE DATABASE IF NOT EXISTS faculdades1;
-- garante que está usando o banco mesmo que o anterior não tenha efeito imediato
ALTER DATABASE faculdades1 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE faculdades1;

-- AQUI começa a criação da tabela
CREATE TABLE alunos (
    aluno_id INT PRIMARY KEY AUTO_INCREMENT,
    nome_aluno VARCHAR(100),
    email_aluno VARCHAR(100),
    curso VARCHAR(100),
    status VARCHAR(50),
    turma VARCHAR(20),
    sexo ENUM('Masculino', 'Feminino', 'Outro'),
    idade INT,
    trabalha BOOLEAN,
    renda_familiar DECIMAL(10,2),
    acompanhamento_medico BOOLEAN,
    tem_filho BOOLEAN,
    estado_civil VARCHAR(50),
    semestre INT,
    bimestre INT,

    aula_1 VARCHAR(100),
    professor_1 VARCHAR(100),
    notas_1 DECIMAL(4,2),
    faltas_1 INT,
    desempenho_1 VARCHAR(50),

    aula_2 VARCHAR(100),
    professor_2 VARCHAR(100),
    notas_2 DECIMAL(4,2),
    faltas_2 INT,
    desempenho_2 VARCHAR(50),

    aula_3 VARCHAR(100),
    professor_3 VARCHAR(100),
    notas_3 DECIMAL(4,2),
    faltas_3 INT,
    desempenho_3 VARCHAR(50),

    aula_4 VARCHAR(100),
    professor_4 VARCHAR(100),
    notas_4 DECIMAL(4,2),
    faltas_4 INT,
    desempenho_4 VARCHAR(50),

    aula_5 VARCHAR(100),
    professor_5 VARCHAR(100),
    notas_5 DECIMAL(4,2),
    faltas_5 INT,
    desempenho_5 VARCHAR(50),

    risco_evasao INT
);

CREATE TABLE alunos_tratados (
    aluno_id INT PRIMARY KEY AUTO_INCREMENT,
    nome_aluno VARCHAR(100),
    email_aluno VARCHAR(100),
    curso VARCHAR(100),
    status VARCHAR(50),
    turma VARCHAR(20),
    sexo ENUM('Masculino', 'Feminino', 'Outro'),
    idade INT,
    trabalha BOOLEAN,
    renda_familiar DECIMAL(10,2),
    acompanhamento_medico BOOLEAN,
    tem_filho BOOLEAN,
    estado_civil VARCHAR(50),
    semestre INT,
    bimestre INT,

    aula_1 VARCHAR(100),
    professor_1 VARCHAR(100),
    notas_1 DECIMAL(4,2),
    faltas_1 INT,
    desempenho_1 VARCHAR(50),

    aula_2 VARCHAR(100),
    professor_2 VARCHAR(100),
    notas_2 DECIMAL(4,2),
    faltas_2 INT,
    desempenho_2 VARCHAR(50),

    aula_3 VARCHAR(100),
    professor_3 VARCHAR(100),
    notas_3 DECIMAL(4,2),
    faltas_3 INT,
    desempenho_3 VARCHAR(50),

    aula_4 VARCHAR(100),
    professor_4 VARCHAR(100),
    notas_4 DECIMAL(4,2),
    faltas_4 INT,
    desempenho_4 VARCHAR(50),

    aula_5 VARCHAR(100),
    professor_5 VARCHAR(100),
    notas_5 DECIMAL(4,2),
    faltas_5 INT,
    desempenho_5 VARCHAR(50),

    risco_evasao INT
);

CREATE USER IF NOT EXISTS 'dbpi'@'%' IDENTIFIED BY 'walker1207';
GRANT ALL PRIVILEGES ON faculdades1.* TO 'dbpi'@'%';
FLUSH PRIVILEGES;

