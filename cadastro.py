from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
import utils

cadastro_bp = Blueprint ('cadastro_bp', __name__)

# Rota para cadastro de usuário
@cadastro_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        tipo = request.form['tipo']

        senha_hash = generate_password_hash(senha)

        if not nome or not email or not senha or not tipo:
            flash('Todos os campos são obrigatórios!')
            return redirect(url_for('sucesso'))

        connection = utils.get_db_connection()
        cursor = connection.cursor()

        # Inserir dados na tabela de usuários
        sql = "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)"
        cursor.execute(sql, (nome, email, senha_hash, tipo))
        connection.commit()

        cursor.close()
        connection.close()

        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('cadastro.html')
