from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash, session
import utils

usuarios_bp = Blueprint ('usuarios_bp', __name__)

# Rota para cadastro de matrículas
@usuarios_bp.route('/matriculas', methods=['POST'])
def matriculas():
    id_usuario = request.form['id_usuario']
    id_curso = request.form['id_curso']
    
    connection = utils.get_db_connection()
    cursor = connection.cursor()
    
    # Inserir dados na tabela de matrículas
    sql = "INSERT INTO matriculas (id_usuario, id_curso) VALUES (?, ?)"
    cursor.execute(sql, (id_usuario, id_curso))
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return redirect(url_for('sucesso'))

# Rota para registrar a conclusão do curso
@usuarios_bp.route('/conclusao_curso', methods=['POST'])
def conclusao_curso():
    id_usuario = request.form['id_usuario']
    id_curso = request.form['id_curso']
    
    connection = utils.get_db_connection()
    cursor = connection.cursor()
    
    # Inserir dados na tabela de conclusão de curso
    sql = "INSERT INTO conclusao_curso (id_usuario, id_curso) VALUES (?, ?)"
    cursor.execute(sql, (id_usuario, id_curso))
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return redirect(url_for('sucesso'))


# Rota pra listar todos usuarios
@usuarios_bp.route('/usuarios/listar')
def listar_usuarios():
    connection = utils.get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('listar_usuarios.html', usuarios=usuarios)