FROM r-base

WORKDIR /app

# Instala dependências do sistema para o rmarkdown e outras libs comuns
RUN apt-get update && apt-get install -y \
    pandoc \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libzmq3-dev \
    libgit2-dev \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    && apt-get clean

# Instala o pacote rmarkdown (e outros se quiser)
RUN R -e "install.packages('rmarkdown', repos='http://cran.rstudio.com')"
RUN R -e "install.packages(c('RMySQL', 'DBI', 'tools', 'dplyr', 'tidyr'), repos='https://cloud.r-project.org/')"
# Cria diretório de trabalho
WORKDIR /app

# Copia apenas o script R para a imagem
COPY limpeza.r /app/limpeza.r

# Define o comando de execução
CMD ["Rscript", "limpeza.r"]