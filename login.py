from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
import utils

login_bp = Blueprint('login_bp', __name__)

# Rota para login de usuário
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha_digitada = request.form['senha']

        # Verifica se os campos de email e senha foram preenchidos
        if not email or not senha_digitada:
            return jsonify({'status': 'error', 'message': 'Por favor, preencha todos os campos.'}), 400

        try:
            # Conectar ao banco de dados
            connection = utils.get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = cursor.fetchone()
        except Exception as e:
            return jsonify({'status': 'error', 'message': f'Ocorreu um erro: {str(e)}'}), 500
        finally:
            cursor.close()
            connection.close()

        # Verificar se o usuário foi encontrado e a senha confere
        if user and check_password_hash(user[3], senha_digitada):  # user[2] deve ser o campo de senha no banco
            # Armazenar os dados do usuário na sessão
            session['user_id'] = user[0]  # user[0] deve ser o ID do usuário
            session['user_type'] = user[3]  # user[3] deve ser o tipo do usuário

            return jsonify({'status': 'success', 'message': 'Login bem-sucedido!'}), 200

        else:
            return jsonify({'status': 'error', 'message': 'Email ou senha inválidos. Tente novamente.'}), 401

    # Caso seja um GET request, retorna o status da requisição
    return jsonify({'status': 'error', 'message': 'Método GET não permitido para login.'}), 405
