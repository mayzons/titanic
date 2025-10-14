import cx_Oracle
import sqlite3
import os
import csv
from utils.logs_escrita import (log_info, log_error)
from utils.caminhos import caminhos


def executa():
    autorizcoes = []
    caminho = caminhos()

    log_info('Iniciado o select no Oracle para Aut Max!')

    oracle_instant_client_dir = caminho['ORACLE_HOME']
    os.environ["PATH"] = f"{oracle_instant_client_dir};{os.environ['PATH']}"

    if not cx_Oracle.clientversion():
        cx_Oracle.init_oracle_client(lib_dir=oracle_instant_client_dir)

    def conexaoDB():
        conn = cx_Oracle.connect(
            user=caminho['USER'],
            password=caminho['PASSWORD'],
            dsn=f'{caminho['DNS']}:{caminho['PORT']}/{caminho['SERVICE']}'
        )
        return conn

    conexao = conexaoDB()
    resultado = conexao.cursor()

    sql = """
    SELECT
        TB0008_CD_CONVENIADO AS Posto,
        TO_CHAR(MAX(TB0110_DT_PEDIDOAUTORIZACAO),
        'MM/DD/YYYY HH24:MI:SS') AS UltimaAutorizacao
    FROM
        CADMO.TB0110_AUTORIZACAO
    WHERE
        TB0110_DT_PEDIDOAUTORIZACAO >= TRUNC(SYSDATE - 5)
        AND TB0025_CD_TIPO = 3
    GROUP BY
        TB0008_CD_CONVENIADO
    """

    resultado.execute(sql)

    rows = resultado.fetchall()

    autorizcoes.clear()
    autorizcoes.extend(rows)

    resultado.close()
    conexao.close()

    log_info(f'O retorno foi de {len(autorizcoes)} linhas')

    return autorizcoes


def insert_sqlite(aut):
    caminho = caminhos()

    resetar_tabela_transacoes()

    # Criar conexão do SQLite
    log_info('Iniciado a Insersão no banco de dados SQL!')

    connsqlite = sqlite3.connect(caminho['BANCOSQLITE'])
    cursorsqlite = connsqlite.cursor()

    cursorsqlite.execute("""
        CREATE TABLE IF NOT EXISTS autorizacoes_max (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            POSTO TEXT, Data TEXT
            );
        """)

    insert_query = """
        INSERT INTO autorizacoes_max (
            POSTO, Data
        ) VALUES (?, ?)
        """

    cursorsqlite.executemany(insert_query, aut)
    connsqlite.commit()
    connsqlite.close()

    log_info(f'Inseridos {len(aut)} registros!')


def exportar_para_csv(dt_arqui_nm, pasta_saida):
    caminho = caminhos()

    log_info('Iniciado a geração do CSV/TXT!')

    conexao = sqlite3.connect(caminho['BANCOSQLITE'])
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT POSTO, Data
        FROM autorizacoes_max
    """)
    rows = cursor.fetchall()

    # Obter os nomes das colunas dinamicamente
    colunas = [descricao[0] for descricao in cursor.description]

    nome_arquivo = dt_arqui_nm

    # Caminho do CSV
    caminho_csv = os.path.join(
        pasta_saida, f"{nome_arquivo}.txt")

    with open(caminho_csv, mode="w", newline="", encoding="utf-8") as arquivo_csv: # NOQA
        writer = csv.writer(arquivo_csv, delimiter=",")

        writer.writerow(colunas)  # Escreve o cabeçalho
        writer.writerows(rows)    # Escreve os dados

    cursor.close()
    conexao.close()

    log_info(f'Inseridos {len(rows)} registros!')


def resetar_tabela_transacoes():
    caminho = caminhos()

    log_info('Iniciando o reset do banco')

    conexao = sqlite3.connect(caminho['BANCOSQLITE'])
    cursor = conexao.cursor()

    try:
        # Apaga todos os registros
        cursor.execute("DELETE FROM autorizacoes_max;")
        conexao.commit()

        # Compacta o banco (libera espaço)
        cursor.execute("VACUUM;")

        # Reseta o autoincremento (se necessário)
        cursor.execute("""UPDATE sqlite_sequence
                            SET seq = 0
                                WHERE name = 'autorizacoes';""")

        conexao.commit()

        log_info('Banco resetado SQLite resetado')

    except Exception as e:
        log_error(f'Erro ao resetar a tabela: {e}')

    finally:
        cursor.close()
        conexao.close()
