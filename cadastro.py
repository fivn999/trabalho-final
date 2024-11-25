from flask import Blueprint, render_template, request, url_for, jsonify, redirect
from werkzeug.security import generate_password_hash
import utils

cadastro_bp = Blueprint('cadastro_bp', __name__)

@cadastro_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        # Verificação de campos obrigatórios
        if not nome or not email or not senha:
            return jsonify({'status': 'error', 'message': 'Todos os campos são obrigatórios!'}), 400

        # Gerar o hash da senha
        senha_hash = generate_password_hash(senha)

        # Conectar ao banco de dados
        connection = utils.get_db_connection()
        cursor = connection.cursor()

        # SQL para inserir dados na tabela de usuários
        sql = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
        try:
            cursor.execute(sql, (nome, email, senha_hash))
            connection.commit()
            # Redireciona para a página de login após cadastro
            return redirect(url_for('login_bp.login'))
        except Exception as e:
            connection.rollback()  # Faz rollback em caso de erro
            return jsonify({'status': 'error', 'message': f'Ocorreu um erro ao cadastrar o usuário: {str(e)}'}), 500
        finally:
            cursor.close()
            connection.close()

    return render_template('cadastro.html')

