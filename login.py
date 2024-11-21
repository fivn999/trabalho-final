from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
import utils

login_bp = Blueprint('login_bp', __name__)

# Rota para login de usuário
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha_digitada = request.form['senha']

        connection = utils.get_db_connection()
        cursor = connection.cursor()

        # Verifica se o usuário existe no banco de dados
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        # Verifica se o usuário foi encontrado e se a senha está correta
        if user and check_password_hash(user[2], senha_digitada):  # user[2] é o campo "senha" no banco
            # Salva as informações do usuário na sessão
            session['user_id'] = user[0]  # Salva o ID do usuário
            session['user_type'] = user[4]  # Salva o tipo do usuário (cliente, admin, etc.)
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('index'))  # Redireciona para a página inicial
        else:
            flash('Email ou senha inválidos. Tente novamente.', 'danger')
            return redirect(url_for('login_bp.login'))  # Redireciona de volta para a página de login

    return render_template('login.html')
