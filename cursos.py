from flask import Blueprint, Flask, render_template, request, jsonify
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
    
    return render_template('cadastrar_curso.html', categorias=categorias)

# Rota para cadastrar cursos
@cursos_bp.route('/cursos', methods=['POST'])
def cadastrar_curso():
    nome = request.form['nome']
    descricao = request.form['descricao']
    categoria_id = request.form['categoria_id']
    
    connection = utils.get_db_connection()
    cursor = connection.cursor()
    
    sql = "INSERT INTO cursos (nome, descricao, categoria_id) VALUES (?, ?, ?)"
    
    try:
        cursor.execute(sql, (nome, descricao, categoria_id))
        connection.commit()
        response = {
            'status': 'success',
            'message': 'Curso cadastrado com sucesso!'
        }
        return jsonify(response), 201

    except Exception as e:
        connection.rollback()
        response = {
            'status': 'error',
            'message': f'Ocorreu um erro ao cadastrar o curso: {str(e)}'
        }
        return jsonify(response), 500

    finally:
        cursor.close()
        connection.close()

@cursos_bp.route('/categorias', methods=['GET'])
def exibir_formulario_categoria():
    return render_template('cadastrar_categoria.html')


# Rota para cadastro de categorias de cursos
@cursos_bp.route('/categorias', methods=['POST'])
def cadastrar_categoria():
    nome = request.form['nome']
    descricao = request.form['descricao']
    
    connection = utils.get_db_connection()
    cursor = connection.cursor()
    
    sql = "INSERT INTO categorias (nome, descricao) VALUES (?, ?)"
    
    try:
        cursor.execute(sql, (nome, descricao))
        connection.commit()
        response = {
            'status': 'success',
            'message': 'Categoria cadastrada com sucesso!'
        }
        return jsonify(response), 201

    except Exception as e:
        connection.rollback()
        response = {
            'status': 'error',
            'message': f'Ocorreu um erro ao cadastrar a categoria: {str(e)}'
        }
        return jsonify(response), 500

    finally:
        cursor.close()
        connection.close()


# Rota pra listar todos os cursos
@cursos_bp.route('/cursos', methods=['GET'])
def listar_cursos():
    connection = utils.get_db_connection()
    cursor = connection.cursor()

    # Consultar todos os cursos na tabela
    sql = "SELECT c.nome, c.descricao, cat.nome AS categoria" \
          "FROM cursos c " \
          "JOIN categorias cat ON c.categoria_id = cat.id " 
    cursor.execute(sql)
    cursos = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('listar_cursos.html', cursos=cursos)