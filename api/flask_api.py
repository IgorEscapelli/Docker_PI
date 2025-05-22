from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import time

app = Flask(__name__)

db_config = {
    'host': 'db',
    'user': 'dbpi',
    'password': 'walker1207',
    'database': 'faculdades1'
}

def tentar_conectar():
    print("Tentando conectar ao banco de dados...")
    for i in range(10):
        try:
            conn = mysql.connector.connect(**db_config)
            conn.close()
            print("Conectado ao banco de dados com sucesso!")
            return
        except Error as e:
            print(f"Tentativa {i+1}/10 falhou: {e}")
            time.sleep(5)
    print("Não foi possível conectar ao banco de dados após 10 tentativas. Encerrando...")
    exit(1)

# Testar conexão antes de iniciar a API
tentar_conectar()

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'ok'})

@app.route('/alunos', methods=['GET'])
def listar_alunos():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM alunos")
        alunos = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(alunos)
    except Error as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/alunos', methods=['POST'])
def adicionar_aluno():
    dados = request.get_json()
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO alunos (nome, data_nascimento, curso_id, turma_id) VALUES (%s, %s, %s, %s)",
            (dados['nome'], dados['data_nascimento'], dados['curso_id'], dados['turma_id'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensagem": "Aluno inserido com sucesso!"}), 201
    except Error as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
