from flask import Flask, render_template, request, redirect, url_for
import mariadb

app = Flask(__name__)

# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'canes'

# Rota para processar o formulário
@app.route('/usuario', methods=['POST'])
def usuarios():
    # Obter dados do formulário
    nome = request.form['nome']
    idade = request.form['idade']
    cpf = request.form['cpf']
    telefone = request.form['telefone']

    
    try:
        # Conectar ao banco de dados
        connection = mariadb.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = connection.cursor()

        # Executar comando SQL para inserir dados
        sql = "INSERT INTO usuario (nome,idade,cpf,telefone) VALUES (?,?,?,?)"
        cursor.execute(sql, (nome,idade,cpf,telefone,))  # Passando como tupla
        connection.commit()  # Commit para salvar no banco

    except mariadb.Error as e:
        # Em caso de erro, imprime a mensagem de erro
        return f"Erro ao conectar com o banco de dados: {e}"

    finally:
        # Fechar a conexão com o banco de dados
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
