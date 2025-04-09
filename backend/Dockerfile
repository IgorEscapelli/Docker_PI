FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install flask pandas matplotlib seaborn

EXPOSE 5000

CMD ["python", "app.py"]
