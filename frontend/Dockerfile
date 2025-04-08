# Usa imagem do Node
FROM node:18

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos de dependência primeiro
COPY package*.json ./

# Instala dependências
RUN npm install

# Copia o restante dos arquivos
COPY . .

# Instala servidor estático
RUN npm install -g serve

# Builda o projeto (se você quiser usar React com `create-react-app`)
# RUN npm run build

# Porta exposta (altere se quiser)
EXPOSE 3000

# Comando para iniciar
CMD ["serve", "-s", "public", "-l", "3000"]
