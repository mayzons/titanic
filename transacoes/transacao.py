import cx_Oracle
import sqlite3
import os
import csv
from utils.logs_escrita import (log_info, log_error)
from utils.caminhos import caminhos


def executa(de, ate):
    transacoes = []
    caminho = caminhos()

    log_info('Iniciado o select no Oracle para Transações!')

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
        TB0008_CD_CONVENIADO,
        TB0153_CD_NSU,
        TB0153_ID_DISPOSITIVO,
        TO_CHAR(tb0153_dt_transacao, 'DD/MM/YYYY HH24:MI') AS DATA,
        tb0153_id_pistaanterior,
        tb0138_cd_produto,
        TB0153_CD_TOKEN,
        tb0153_cd_placadispositivo,
        tb0153_cd_placaocr,
        tb0153_cd_cupomfiscal,
        tb0153_vl_transacao
    FROM
        CADMO.tb0153_transacaoconveniado
    WHERE
        tb0153_dt_transacao
        BETWEEN TO_TIMESTAMP(:data_de, 'DD/MM/YYYY HH24:MI')
            AND TO_TIMESTAMP(:data_ate, 'DD/MM/YYYY HH24:MI')
        AND tb0138_cd_produto = '1'
    ORDER BY tb0153_dt_transacao DESC
    """

    data_de_str = de.strftime('%d/%m/%Y %H:%M')
    data_ate_str = ate.strftime('%d/%m/%Y %H:%M')

    resultado.execute(sql, {'data_de': data_de_str, 'data_ate': data_ate_str})
    rows = resultado.fetchall()

    transacoes.clear()
    transacoes.extend(rows)

    resultado.close()
    conexao.close()

    log_info(f'O Select retornou {len(transacoes)} Transações!')

    return transacoes


def insert_sqlite(transac):
    resetar_tabela_transacoes()
    caminho = caminhos()

    # Criar conexão do SQLite
    log_info('Iniciado a Insersão no banco de dados SQL!')

    connsqlite = sqlite3.connect(caminho['BANCOSQLITE'])
    cursorsqlite = connsqlite.cursor()

    cursorsqlite.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        POSTO TEXT,
        NSU TEXT,
        TAG TEXT,
        DATA TEXT,
        BOMBA TEXT,
        CODIGO_PRODUTO TEXT,
        TIPO_APROVAO TEXT,
        PLACA_CAD TEXT,
        PLACA_OCR TEXT,
        TIPOTRN TEXT,
        VALOR_TRN REAL
    )
    """)

    insert_query = """
        INSERT INTO transacoes (
            POSTO, NSU, TAG, DATA, BOMBA, CODIGO_PRODUTO,
            TIPO_APROVAO, PLACA_CAD, PLACA_OCR,
            TIPOTRN, VALOR_TRN
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    cursorsqlite.executemany(insert_query, transac)
    connsqlite.commit()
    connsqlite.close()

    log_info(f'{len(transac)} registros inseridos no SQLite com sucesso!')


def exportar_para_csv(dt_arqui_nm, pasta_saida):
    caminho = caminhos()

    log_info('Iniciado a geração do CSV/TXT!')

    conexao = sqlite3.connect(caminho['BANCOSQLITE'])
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM transacoes
    """)
    rows = cursor.fetchall()

    nome_arquivo = dt_arqui_nm

    # Caminho do CSV
    caminho_csv = os.path.join(pasta_saida, f"{nome_arquivo}.txt")

    with open(
            caminho_csv, mode="w", newline="",
            encoding="utf-8") as arquivo_csv:
        writer = csv.writer(arquivo_csv, delimiter="|")

        # writer.writerow(colunas)  # Escreve o cabeçalho
        writer.writerows(rows)    # Escreve os dados

    cursor.close()
    conexao.close()

    log_info(f'CSV gerado com sucesso com {len(rows)} registros!')


def resetar_tabela_transacoes():
    caminho = caminhos()

    log_info('Iniciando o reset do banco SQL para autorizações!')

    conexao = sqlite3.connect(caminho['BANCOSQLITE'])
    cursor = conexao.cursor()

    try:
        cursor.execute("DELETE FROM transacoes;")
        conexao.commit()
        cursor.execute("VACUUM;")
        cursor.execute(
            """
            UPDATE sqlite_sequence SET seq = 0 WHERE name = 'transacoes'
            """)
        conexao.commit()

        log_info('Banco resetado SQLite resetado para Transações')

    except Exception as e:
        log_error(f'Erro ao resetar a tabela: {e}')

    finally:
        cursor.close()
        conexao.close()
