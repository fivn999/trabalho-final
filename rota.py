from flask import Flask, render_template, request, redirect, url_for
import mariadb

app = Flask(__name__)

# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'canes'

# Rota para processar o formulário
@app.route('/cursos', methods=['POST'])
def cursos():
    # Obter dados do formulário
    nome = request.form['nome']
    # Inserir dados no banco de dados
    connection = mariadb.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    cursor = connection.cursor()

    # Executar comando SQL para inserir dados
    sql = "INSERT INTO produtos (nome) VALUES (?)"
    cursor.execute(sql, (nome))
    connection.commit()

    # Fechar conexão com o banco de dados
    cursor.close()
    connection.close()

    # Redirecionar para página de sucesso ou outra página
    return redirect(url_for('sucesso'))

# Rota para página de sucesso
@app.route('/sucesso')
def sucesso():
    return 'Dados inseridos com sucesso!'

if __name__ == '__main__':
    app.run(debug=True)