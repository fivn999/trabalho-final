import mariadb
import logging

db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'canes'

def get_db_connection():
    try:
        return mariadb.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    except mariadb.Error as e:
        logging.error(f"Erro de conexão ao banco de dados: {e}")
        raise
