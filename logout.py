from flask import Blueprint, request, jsonify, session

logout_bp = Blueprint('logout_bp', __name__)

# Rota para logout
@logout_bp.route('/logout')
def logout():
    # Verifica se o usuário está autenticado antes de tentar desconectar
    if 'user_id' in session:
        session.pop('user_id', None)  # Remove o ID do usuário da sessão
        session.pop('user_type', None)  # Remove o tipo de usuário da sessão
        
        # Retorna uma resposta de sucesso em JSON
        return jsonify({'status': 'success', 'message': 'Você foi desconectado.'}), 200
    else:
        # Se o usuário não estiver autenticado, retorna um erro
        return jsonify({'status': 'error', 'message': 'Nenhum usuário está autenticado.'}), 400
