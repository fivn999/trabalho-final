from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import mariadb
import hashlib

app = Flask(__name__)
app.secret_key = 'secret_key'

# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'reservas_hotel'

# Função para conectar ao banco de dados
def get_db_connection():
    conn = mariadb.connect(
        host=db_host, user=db_user, password=db_password, database=db_name
    )
    return conn

# Rota para cadastro de usuário
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = hashlib.sha256(request.form['senha'].encode()).hexdigest()  # Criptografando a senha

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (nome, email, senha, tipo) VALUES (%s, %s, %s, %s)', (nome, email, senha, 'cliente'))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('cadastro.html')

# Rota para login de usuário
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = hashlib.sha256(request.form['senha'].encode()).hexdigest()  # Criptografando a senha

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = %s AND senha = %s', (email, senha))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['user_type'] = user[4]
            return redirect(url_for('index'))
        else:
            return 'Login falhou. Verifique suas credenciais.', 401

    return render_template('login.html')

# Página inicial - exibe a disponibilidade de quartos/mesas
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM disponibilidade WHERE disponivel = TRUE')
    disponibilidade = cursor.fetchall()
    conn.close()
    return render_template('index.html', disponibilidade=disponibilidade)

# Rota para fazer reserva
@app.route('/reservar/<int:id>', methods=['POST'])
def reservar(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM disponibilidade WHERE id = %s', (id,))
    disponibilidade = cursor.fetchone()

    if disponibilidade and disponibilidade[4] == True:  # Se a disponibilidade for verdadeira
        cursor.execute('INSERT INTO reservas (usuario_id, disponibilidade_id, data_reserva, status) VALUES (%s, %s, NOW(), %s)',
                       (session['user_id'], id, 'pendente'))
        cursor.execute('UPDATE disponibilidade SET disponivel = FALSE WHERE id = %s', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        conn.close()
        return 'Desculpe, essa opção de reserva não está mais disponível.', 404

# Rota para exibir reservas do usuário
@app.route('/minhas_reservas')
def minhas_reservas():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reservas WHERE usuario_id = %s', (session['user_id'],))
    reservas = cursor.fetchall()
    conn.close()

    return render_template('minhas_reservas.html', reservas=reservas)

if __name__ == '__main__':
    app.run(debug=True)
