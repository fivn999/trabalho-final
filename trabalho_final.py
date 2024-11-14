from flask import Flask, render_template, request, redirect, url_for
import mariadb

app = Flask(__name__)

# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'canes'

# Função para conectar ao banco de dados
def get_db_connection():
    return mariadb.connect(host=db_host, user=db_user, password=db_password, database=db_name)

# Rota para cadastro de usuários
@app.route('/usuarios', methods=['POST'])
def usuarios():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    tipo = request.form['tipo']
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Inserir dados na tabela de usuários
    sql = "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)"
    cursor.execute(sql, (nome, email, senha, tipo))
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return redirect(url_for('sucesso'))

# Rota para cadastrar cursos
@app.route('/cursos', methods=['POST'])
def cadastrar_curso():
    nome = request.form['nome']
    descricao = request.form['descricao']
    preco = request.form['preco']
    categoria_id = request.form['categoria_id']
    id_instrutor = request.form['id_instrutor']
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Inserir dados na tabela de cursos
    sql = "INSERT INTO cursos (nome, descricao, preco, categoria_id, id_instrutor) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(sql, (nome, descricao, preco, categoria_id, id_instrutor))
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return redirect(url_for('sucesso'))

# Rota para cadastro de categorias de cursos
@app.route('/categorias', methods=['POST'])
def cadastrar_categoria():
    nome = request.form['nome']
    descricao = request.form['descricao']
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Inserir dados na tabela de categorias
    sql = "INSERT INTO categorias (nome, descricao) VALUES (?, ?)"
    cursor.execute(sql, (nome, descricao))
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return redirect(url_for('sucesso'))

# Rota para cadastro de matrículas
@app.route('/matriculas', methods=['POST'])
def matriculas():
    id_usuario = request.form['id_usuario']
    id_curso = request.form['id_curso']
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Inserir dados na tabela de matrículas
    sql = "INSERT INTO matriculas (id_usuario, id_curso) VALUES (?, ?)"
    cursor.execute(sql, (id_usuario, id_curso))
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return redirect(url_for('sucesso'))

# Rota para registro de pagamentos
@app.route('/pagamentos', methods=['POST'])
def pagamentos():
    id_usuario = request.form['id_usuario']
    id_curso = request.form['id_curso']
    valor = request.form['valor']
    metodo_pagamento = request.form['metodo_pagamento']
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Inserir dados na tabela de pagamentos
    sql = "INSERT INTO pagamentos (id_usuario, id_curso, valor, metodo_pagamento) VALUES (?, ?, ?, ?)"
    cursor.execute(sql, (id_usuario, id_curso, valor, metodo_pagamento))
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return redirect(url_for('sucesso'))

# Rota para adicionar comentários
@app.route('/comentarios', methods=['POST'])
def comentarios():
    id_usuario = request.form['id_usuario']
    id_curso = request.form['id_curso']
    comentario = request.form['comentario']
    nota = request.form['nota']
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Inserir dados na tabela de comentários
    sql = "INSERT INTO comentarios (id_usuario, id_curso, comentario, nota) VALUES (?, ?, ?, ?)"
    cursor.execute(sql, (id_usuario, id_curso, comentario, nota))
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return redirect(url_for('sucesso'))

# Rota para adicionar aulas a um curso
@app.route('/aulas', methods=['POST'])
def aulas():
    id_curso = request.form['id_curso']
    titulo = request.form['titulo']
    video_url = request.form['video_url']
    descricao = request.form['descricao']
    ordem = request.form['ordem']
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Inserir dados na tabela de aulas
    sql = "INSERT INTO aulas (id_curso, titulo, video_url, descricao, ordem) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(sql, (id_curso, titulo, video_url, descricao, ordem))
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return redirect(url_for('sucesso'))

# Rota para registrar a conclusão do curso
@app.route('/conclusao_curso', methods=['POST'])
def conclusao_curso():
    id_usuario = request.form['id_usuario']
    id_curso = request.form['id_curso']
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Inserir dados na tabela de conclusão de curso
    sql = "INSERT INTO conclusao_curso (id_usuario, id_curso) VALUES (?, ?)"
    cursor.execute(sql, (id_usuario, id_curso))
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return redirect(url_for('sucesso'))

# Rota para página de sucesso
@app.route('/sucesso')
def sucesso():
    return 'Dados inseridos com sucesso!'

# Rota para listar todos os usuários
@app.route('/usuarios/listar')
def listar_usuarios():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('listar_usuarios.html', usuarios=usuarios)

# Rota para listar todos os cursos
@app.route('/cursos/listar')
def listar_cursos():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM cursos")
    cursos = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('listar_cursos.html', cursos=cursos)

if __name__ == '__main__':
    app.run(debug=True)










