from flask import Blueprint, Flask, request, render_template, redirect, url_for, flash, session


logout_bp = Blueprint('login_bp', __name__)

# Rota para logout
@logout_bp.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove o ID do usuário da sessão
    session.pop('user_type', None)  # Remove o tipo de usuário da sessão
    flash('Você foi desconectado.', 'success')
    return redirect(url_for('login_bp.login'))  # Redireciona para a página de login