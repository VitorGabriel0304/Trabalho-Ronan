# db.py — Módulo central de acesso ao banco de dados
import mysql.connector
from mysql.connector import Error, pooling
import os

# Parâmetros de conexão
_DB_PARAMS = {
    'host':               '127.0.0.1',
    'user':               'root',
    'password':           '',
    'database':           'cinelist',
    'charset':            'utf8mb4',
    'use_pure':           True,
    'connection_timeout': 5,
    'autocommit':         False,
}

_pool = None

def criar_pool():
    global _pool
    if _pool is None:
        try:
            _pool = pooling.MySQLConnectionPool(
                pool_name='webapp_pool',
                pool_size=5,
                pool_reset_session=True,
                **_DB_PARAMS
            )
        except Error as e:
            print(f"Aviso: Não foi possível criar o pool de conexões MySQL: {e}")
            _pool = None
    return _pool

def get_connection():
    global _pool
    if _pool is None:
        criar_pool()
    if _pool is None:
        raise Exception("MySQL não está disponível no momento.")
    try:
        return _pool.get_connection()
    except Error as e:
        raise Exception(f'Não foi possível obter conexão do pool: {e}')

def execute_query(sql, params=None, fetch=False):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params or ())

        if fetch:
            res = cursor.fetchall()
            cursor.close()
            conn.close()
            return res
        else:
            conn.commit()
            count = cursor.rowcount
            cursor.close()
            conn.close()
            return count
    except Exception as e:
        print(f"Erro na query: {e}")
        # Se falhar o BD, retornamos vazio para não quebrar o app
        return [] if fetch else 0

def execute_one(sql, params=None):
    resultados = execute_query(sql, params, fetch=True)
    return resultados[0] if resultados and isinstance(resultados, list) else None

def iniciar_bd():
    try:
        conn = mysql.connector.connect(
            host = '127.0.0.1',
            user = 'root',
            password = '',
            connection_timeout=5
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS cinelist CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        cursor.execute("USE cinelist;")

        arquivo_sql = os.path.join(os.path.dirname(__file__), 'schema.sql')
        if os.path.exists(arquivo_sql):
            with open(arquivo_sql, 'r', encoding='utf-8' ) as f:
                script_sql = f.read()

            for stmt in script_sql.split(';'):
                stmt = stmt.strip()
                if stmt and not stmt.upper().startswith('CREATE DATABASE') and not stmt.upper().startswith('USE'):
                    try:
                        cursor.execute(stmt)
                    except Exception as e:
                        pass
        
        conn.commit()
        cursor.close()
        conn.close()
        print('Banco e tabelas inicializadas com sucesso')
    except Exception as e:
        print(f"Aviso: Banco de dados não inicializado (MySQL offline): {e}")
