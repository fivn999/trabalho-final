from flask import Flask, request, render_template, redirect, url_for, flash, session
import utils

from cadastro import cadastro_bp
from cursos import cursos_bp
from usuarios import usuarios_bp
from login import login_bp

app = Flask(__name__)

app.secret_key = 'canes'

app.register_blueprint(cadastro_bp)
app.register_blueprint(cursos_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(login_bp)

# INDEX
@app.route('/')
def index():
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return render_template('login.html')  # Redireciona para a página de login se não estiver autenticado

    # Se o usuário estiver autenticado, exibe a página inicial
    connection = utils.get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM disponibilidade WHERE disponivel = TRUE')
    disponibilidade = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('index.html', disponibilidade=disponibilidade)

# Rota para página de sucesso
@app.route('/sucesso')
def sucesso():
    tipo = request.args.get('tipo') 
    return render_template('sucesso.html', tipo=tipo)

if __name__ == '__main__':
    app.run(debug=True)
