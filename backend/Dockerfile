FROM python:3.10

WORKDIR /app

# Copia só o requirements primeiro (melhora cache)
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Agora copia o restante da aplicação
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
