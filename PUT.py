from flask import Flask, jsonify, render_template, request, redirect, url_for
import mariadb

app = Flask(__name__)

# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'canes'

# Rota para processar o formulário
@app.route('/usuario/<int:usuario_id>', methods=['PUT'])
def atualizar_usuario(usuario_id):
    # Obter os dados do formulário
    dados = request.json  # Assumindo que os dados são enviados em formato JSON

    # Validar os dados (exemplo básico)
    if 'nome' not in dados or 'idade' not in dados or 'cpf' not in dados or 'telefone' not in dados:
        return jsonify({'error': 'Faltando dados obrigatórios!'}), 400

    # Construir a consulta SQL para atualizar os dados
    sql = "UPDATE usuario SET nome=%s, idade=%s, cpf=%s, telefone=%s WHERE id=%s"
    valores = (dados['nome'], dados['idade'], dados['cpf'], dados['telefone'], usuario_id)

    try:
        # Conectar ao banco de dados MariaDB
        conn = mariadb.connect(
            host=db_host, user=db_user, password=db_password, database=db_name
        )
        cursor = conn.cursor()

        # Executar a consulta SQL
        cursor.execute(sql, valores)

        # Verificar se a atualização foi bem-sucedida
        if cursor.rowcount == 0:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        # Commit da transação
        conn.commit()

        return jsonify({'mensagem': 'Usuário atualizado com sucesso'}), 200

    except mariadb.Error as error:
        return jsonify({'error': str(error)}), 500

    finally:
        # Fechar a conexão e o cursor
        if cursor:
            cursor.close()
        if conn:
            conn.close()


    # Redirecionar para página de sucesso ou outra página
    #return redirect(url_for('sucesso'))

# Rota para página de sucesso
@app.route('/sucesso')
def sucesso():
    return 'Dados inseridos com sucesso!'

if __name__ == '__main__':
    app.run(debug=True)
