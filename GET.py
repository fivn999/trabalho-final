from flask import Flask, jsonify, render_template, request, redirect, url_for
import mariadb

app = Flask(__name__)

# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'canes'

# Rota para processar o formulário
@app.route('/usuario', methods=['GET'])
def listar_usuarios():
    try:
        # Conectar ao banco de dados MariaDB
        connection = mariadb.connect(
            host=db_host, user=db_user, password=db_password, database=db_name
        )
        cursor = connection.cursor()

        # Executar a consulta SQL para selecionar todos os usuários
        sql = "SELECT * FROM usuario"
        cursor.execute(sql)

        # Obter os resultados da consulta
        resultados = cursor.fetchall()

        # Formatar os resultados em um JSON
        usuarios = []
        for usuario in resultados:
            usuarios.append({'id': usuario[0], 'nome': usuario[1], 'email': usuario[2], 'idade': usuario[3]})

        return jsonify({'usuarios': usuarios}), 200
    except mariadb.Error as error:
        return jsonify({'error': str(error)}), 500
    finally:
        if connection:
            connection.close()

    # Redirecionar para página de sucesso ou outra página
    #return redirect(url_for('sucesso'))

# Rota para página de sucesso
@app.route('/sucesso')
def sucesso():
    return 'Dados inseridos com sucesso!'

if __name__ == '__main__':
    app.run(debug=True)
