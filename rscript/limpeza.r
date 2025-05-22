# processa_dados.R

library(DBI)
library(RMySQL)
library(dplyr)
library(tidyr)
library(tools)

# Conexão ao banco de dados
con = dbConnect(MySQL(),
                 host = "db",
                 user = "dbpi",
                 password = "walker1207",
                 dbname = "faculdades1")

# Leitura dos dados não processados
query = "SELECT * FROM alunos WHERE processado = 0"
dados = dbGetQuery(con, query)

if (nrow(dados) > 0) {

  # Renomeando colunas (ajuste conforme necessário)
  colnames(dados) = c(
    "ID", "Nome", "Email", "Curso", "Status", "Turma", "Sexo", "Idade", 
    "Trabalha", "Renda", "Acompanhamento_Medico", "Tem_Filho", "Estado_Civil", 
    "Semestre", "Bimestre", 
    "Aula_1", "Professor_1", "Nota_1", "Falta_Materia_1", "Desempenho_1", 
    "Aula_2", "Professor_2", "Nota_2", "Falta_Materia_2", "Desempenho_2", 
    "Aula_3", "Professor_3", "Nota_3", "Falta_Materia_3", "Desempenho_3", 
    "Aula_4", "Professor_4", "Nota_4", "Falta_Materia_4", "Desempenho_4", 
    "Aula_5", "Professor_5", "Nota_5", "Falta_Materia_5", "Desempenho_5"
  )

  limpar_nomes = function(dados) {
    dados$Nome = as.character(dados$Nome)
    dados$Email = as.character(dados$Email)
    nomes_invalidos = c("Desconhecido", "NULL", "#######", "0923023", "user", "notexist", "22333123", "?", "", "none.com")
    regex_nome_valido = "^[A-Za-zÀ-ÿ ]{2,}$"
    nome_do_email = sub("@.*", "", dados$Email)
    nome_invalido_logico = (
      is.na(dados$Nome) |
      dados$Nome %in% nomes_invalidos |
      !grepl(regex_nome_valido, dados$Nome)
    )
    nome_email_valido = grepl(regex_nome_valido, nome_do_email)
    substituir_nome = nome_invalido_logico & nome_email_valido
    dados$Nome[substituir_nome] = nome_do_email[substituir_nome]
    nome_invalido_final = (
      is.na(dados$Nome) |
      dados$Nome %in% nomes_invalidos |
      !grepl(regex_nome_valido, dados$Nome)
    )
    dados = dados[!nome_invalido_final, ]
    nome_suspeito = grepl("^[a-z]+$", dados$Nome) & !grepl(" ", dados$Nome)
    dados = dados[!nome_suspeito, ]
    dados$Nome = gsub("\\b(Sr\\.|Sra\\.|Dr\\.|Dra\\.)\\s*", "", dados$Nome)
    dados$Nome = tools::toTitleCase(tolower(dados$Nome))
    return(dados)
  }

  limpar_emails = function(dados) {
    dados$Email = as.character(dados$Email)
    regex_email_valido = "^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$"
    emails_invalidos = c("@email", "NULL", "#######", "XX0294393LLL", "user", "notexist", "22333123", "?", "", "none.com")
    email_invalido_logico = (
      is.na(dados$Email) |
      dados$Email %in% emails_invalidos |
      !grepl(regex_email_valido, dados$Email)
    )
    dados$Email[email_invalido_logico] = NA
    nome_limpo = tolower(gsub(" ", "", dados$Nome))
    dados$Email[is.na(dados$Email)] = paste0(nome_limpo[is.na(dados$Email)], "@unifeob.com")
    dados$Email = tolower(dados$Email)
    return(dados)
  }
  
  limpar_cursos = function(dados) {
    dados$Curso = as.character(dados$Curso)
    insercoes = c('Administração', 'Direito', 'Engenharia', 'Pedagogia', 'Psicologia', 'Engenharia Civil', 'Engenharia Elétrica', 'Engenharia Mecânica', 'Engenharia de Produção', 'Arquitetura e Urbanismo', 'Medicina', 'Enfermagem', 'Biomedicina', 'Educação Física', 'Fisioterapia', 'Odontologia', 'Farmácia', 'Veterinária', 'Nutrição', 'Computação', 'Ciência da Computação', 'Sistemas de Informação', 'Análise e Desenvolvimento de Sistemas', 'Jogos Digitais', 'Redes de Computadores', 'Banco de Dados', 'Matemática', 'Física', 'Química', 'Biologia', 'Geografia', 'História', 'Letras', 'Serviço Social', 'Relações Internacionais', 'Jornalismo', 'Publicidade e Propaganda', 'Design Gráfico', 'Marketing', 'Recursos Humanos', 'Engenharia Ambiental', 'Engenharia de Alimentos', 'Engenharia Química', 'Zootecnia', 'Gastronomia', 'Moda', 'Teatro', 'Música', 'Dança', 'Cinema', 'Artes Visuais', 'Ciências Contábeis', 'Ciências Econômicas', 'Teologia', 'Fonoaudiologia', 'Terapia Ocupacional', 'Gestão Pública', 'Gestão Comercial', 'Logística', 'Secretariado Executivo', 'Turismo', 'Hotelaria', 'Ciências Sociais', 'Estatística', 'Biblioteconomia', 'Museologia', 'Educação Especial', 'Segurança do Trabalho', 'Radiologia')
    i = 1
    
    while (sum(is.na(dados$Curso)) > 0) {
      
      posicao = which(is.na(dados$Curso))[1]
      dados$Curso[posicao] = insercoes[i]
      
      i = i + 1
      if(i > lenght(insercoes)) {
        i = 1
      }
    }
  }
  
  limpar_sexo = function(dados) {
    dados$Sexo = tolower(dados$Sexo)
    dados$Sexo[dados$Sexo %in% c("masculino", "masc", "m")] = "masculino"
    dados$Sexo[dados$Sexo %in% c("feminino", "fem", "feminno")] = "feminino"
    dados$Sexo[!dados$Sexo %in% c("masculino", "feminino")] = NA
    
    sexo_tab = table(dados$Sexo)
    if (length(sexo_tab) >= 2) {
      sexo_prop = as.numeric(sexo_tab) / sum(sexo_tab)
      sexo_names = names(sexo_tab)
      n_na = sum(is.na(dados$Sexo))
      set.seed(123)
      dados$Sexo[is.na(dados$Sexo)] = sample(sexo_names, size = n_na, replace = TRUE, prob = sexo_prop)
    } else {
      warning("Não há dados suficientes para aplicar o rateio proporcional em Sexo.")
    }
  }
  
  limpar_idade = function(dados) {
    dados$Idade = as.numeric(as.character(dados$Idade))
    mediana_idade = median(dados$Idade[dados$Idade >= 17 & dados$Idade <= 80], na.rm = TRUE)
    dados$Idade[dados$Idade < 17 | dados$Idade > 80 | is.na(dados$Idade)] <- mediana_idade
  }
  
  limpar_renda = function(dados) {
    dados$Renda = as.numeric(as.character(dados$Renda))
    
    # Calculo usando Intervalo Interquantil (IQR)
    Q1_renda <- quantile(dados$Renda, 0.25, na.rm = TRUE)
    Q3_renda <- quantile(dados$Renda, 0.75, na.rm = TRUE)
    IQR_renda <- Q3_renda - Q1_renda
    limite_inferior_renda <- Q1_renda - 1.5 * IQR_renda
    limite_superior_renda <- Q3_renda + 1.5 * IQR_renda
    mediana_renda <- median(dados$Renda[dados$Renda >= limite_inferior_renda & dados$Renda <= limite_superior_renda], na.rm = TRUE)
    
    # Substituir outliers por mediana
    dados$Renda[dados$Renda < limite_inferior_renda | dados$Renda > limite_superior_renda | is.na(dados$Renda)] <- mediana_renda
  }
  
  limpar_estado_civil = function(dados) {
    dados$`Estado Civil` <- tolower(trimws(dados$`Estado Civil`))
    
    dados$`Estado Civil`[dados$`Estado Civil` %in% c("solteiro", "solteira", "s")] <- "solteiro"
    dados$`Estado Civil`[dados$`Estado Civil` %in% c("casado", "casada", "c", "casadoo")] <- "casado"
    dados$`Estado Civil`[dados$`Estado Civil` %in% c("divorciado", "divorciada", "d")] <- "divorciado"
    dados$`Estado Civil`[dados$`Estado Civil` %in% c("viuvo", "viúva", "v")] <- "viuvo"
    
    dados$`Estado Civil`[!dados$`Estado Civil` %in% c("solteiro", "casado", "divorciado", "viuvo")] <- NA
    
    estado_tab <- table(dados$`Estado Civil`)
    if (length(estado_tab) >= 2) {
      estado_prop <- as.numeric(estado_tab) / sum(estado_tab)
      estado_names <- names(estado_tab)
      
      n_na_estado <- sum(is.na(dados$`Estado Civil`))
      
      set.seed(456)  # Diferente seed para rastreabilidade
      dados$`Estado Civil`[is.na(dados$`Estado Civil`)] <- sample(estado_names,
                                                                  size = n_na_estado,
                                                                  replace = TRUE,
                                                                  prob = estado_prop)
    } else {
      warning("Não há dados suficientes para aplicar o rateio proporcional em Estado Civil.")
    }
  }
  
  # Aplicar limpeza
  dados = limpar_nomes(dados)
  dados = limpar_emails(dados)
  dados = limpar_cursos(dados)
  dados = limpar_sexo(dados)
  dados = limpar_idade(dados)
  dados = limpar_renda(dados)
  dados = limpar_estado_civil(dados)

  # Tratamento de valores ausentes
  dados = dados %>%
    mutate(across(everything(), ~ replace_na(., 0)))

  # Lógica de risco de evasão
  calcula_risco = function(linha) {
    notas = unlist(linha[grep("Nota_", names(linha))])
    faltas = unlist(linha[grep("Falta_Materia_", names(linha))])
    if (mean(as.numeric(notas)) < 6 || any(as.numeric(faltas) > 5)) {
      return(1)
    } else {
      return(0)
    }
  }

  dados$Risco_de_Evasao = apply(dados, 1, calcula_risco)

  # Grava os dados tratados
  dbWriteTable(con, "alunos_tratados", dados, append = TRUE, row.names = FALSE)

  # Atualiza como processado
  ids = paste(dados$ID, collapse = ",")
  dbExecute(con, sprintf("UPDATE alunos_raw SET processado = 1 WHERE ID IN (%s)", ids))

  cat(paste(Sys.time(), "- Processados", nrow(dados), "registros.\n"))

} else {
  cat(paste(Sys.time(), "- Nenhum novo registro encontrado.\n"))
}

dbDisconnect(con)