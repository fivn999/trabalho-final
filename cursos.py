from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash, session
import utils

cursos_bp = Blueprint ('cursos_bp', __name__)


@cursos_bp.route('/cursos', methods=['GET'])
def exibir_formulario():
    # Conexão ao banco para obter categorias existentes
    connection = utils.get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, nome FROM categorias")
    categorias = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template('cadastrar_curso.html', categorias=categorias)  # Passa as categorias para o template

# Rota para cadastrar cursos
@cursos_bp.route('/cursos', methods=['POST'])
def cadastrar_curso():
    nome = request.form['nome']
    descricao = request.form['descricao']
    categoria_id = request.form['categoria_id']
    id_instrutor = request.form['id_instrutor']
    
    connection = utils.get_db_connection()
    cursor = connection.cursor()
    
    # Inserir dados na tabela de cursos
    sql = "INSERT INTO cursos (nome, descricao, categoria_id, id_instrutor) VALUES (?, ?, ?, ?)"
    cursor.execute(sql, (nome, descricao, categoria_id, id_instrutor))
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return redirect(url_for('sucesso', tipo = 'cadastrar_curso'))


@cursos_bp.route('/categorias', methods=['GET'])
def exibir_formulario_categoria():
    return render_template('cadastrar_categoria.html')  # Renderiza a página de cadastro de categoria


# Rota para cadastro de categorias de cursos
@cursos_bp.route('/categorias', methods=['POST'])
def cadastrar_categoria():
    nome = request.form['nome']
    descricao = request.form['descricao']
    
    connection = utils.get_db_connection()
    cursor = connection.cursor()
    
    sql = "INSERT INTO categorias (nome, descricao) VALUES (?, ?)"
    cursor.execute(sql, (nome, descricao))
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return redirect(url_for('sucesso', tipo='cadastrar_categoria'))


# Rota pra listar todos os cursos
@cursos_bp.route('/cursos', methods=['GET'])
def listar_cursos():
    connection = utils.get_db_connection()
    cursor = connection.cursor()

    # Consultar todos os cursos na tabela
    sql = "SELECT c.nome, c.descricao, cat.nome AS categoria, i.nome AS instrutor " \
          "FROM cursos c " \
          "JOIN categorias cat ON c.categoria_id = cat.id " \
          "JOIN instrutores i ON c.id_instrutor = i.id"
    cursor.execute(sql)
    cursos = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('listar_cursos.html', cursos=cursos)