import cx_Oracle
import sqlite3
import os
import csv
from utils.logs_escrita import (log_info, log_error)
from utils.caminhos import caminhos


def executa(de, ate):
    autorizcoes = []
    caminho = caminhos()

    log_info('# Iniciado o select no Oracle para Autorizações!')

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
        TB0008_CD_CONVENIADO AS POSTO,
        TO_CHAR(TB0110_DT_PEDIDOAUTORIZACAO, 'DD/MM/YYYY HH24:MI') AS Data,
        TB0138_CD_PRODUTO AS Produto,
        TB0110_ID_DISPOSITIVO as Dispositivo,
        TB0110_NR_PLACAVEICULO as Placa,
        TB0110_VL_SALDODISPONIVEL as Saldo,
        TB0110_FL_RESULTADO AS Resultado,
        TB0025_CL_CDMOTIVOREJEICAO As "Cod. Rejeicao",
        TB0025_CD_MOTIVOREJEICAO As "Mot. Rejeicao",
        TB0110_CD_TOKEN AS TP_SOLICITACAO,
        TB0110_VL_SALDODIARIODISP AS SALDO_DIARIO,
        TB0100_ID_PEDIDO AS ID_PEDIDO,
        TB0110_CD_AUTHEXCEPT AS WL_LIBERADO
    FROM
        CADMO.TB0110_AUTORIZACAO
    WHERE
        TB0110_DT_PEDIDOAUTORIZACAO
                    BETWEEN TO_TIMESTAMP(:data_de, 'DD/MM/YYYY HH24:MI')
                            AND TO_TIMESTAMP(:data_ate, 'DD/MM/YYYY HH24:MI')
        AND TB0025_CD_TIPO = 3
    ORDER BY
        TB0110_DT_PEDIDOAUTORIZACAO DESC
    """

    data_de_str = de.strftime('%d/%m/%Y %H:%M')
    data_ate_str = ate.strftime('%d/%m/%Y %H:%M')

    resultado.execute(sql, {'data_de': data_de_str, 'data_ate': data_ate_str})

    rows = resultado.fetchall()

    autorizcoes.clear()
    autorizcoes.extend(rows)

    resultado.close()
    conexao.close()

    log_info(f'Total de autorizações {len(autorizcoes)}')

    return autorizcoes


def insert_sqlite(aut):
    caminho = caminhos()

    resetar_tabela_transacoes()

    # Criar conexão do SQLite
    log_info('# Iniciado a Insersão no banco de dados SQL!')

    connsqlite = sqlite3.connect(caminho['BANCOSQLITE'])
    cursorsqlite = connsqlite.cursor()

    cursorsqlite.execute("""
        CREATE TABLE IF NOT EXISTS autorizacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            POSTO TEXT, Data TEXT, Produto TEXT,
            Dispositivo TEXT, Placa TEXT, Saldo REAL,
            Resultado TEXT, "Cod. Rejeicao" TEXT,
            "Mot. Rejeicao" TEXT, TP_SOLICITACAO TEXT,
            SALDO_DIARIO REAL, ID_PEDIDO TEXT, WL_LIBERADO TEXT
        );
        """)

    insert_query = """
        INSERT INTO autorizacoes (
            POSTO, Data, Produto, Dispositivo, Placa, Saldo,
            Resultado, "Cod. Rejeicao", "Mot. Rejeicao",
            TP_SOLICITACAO, SALDO_DIARIO, ID_PEDIDO, WL_LIBERADO
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

    cursorsqlite.executemany(insert_query, aut)
    connsqlite.commit()
    connsqlite.close()

    log_info(f'Total de linhas adiconadas ao banco {len(aut)}')


def exportar_para_csv(dt_arqui_nm, pasta_saida):
    caminho = caminhos()

    log_info('Iniciado a geração do CSV/TXT!')

    conexao = sqlite3.connect(caminho['BANCOSQLITE'])
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT POSTO, Data, Produto, Dispositivo, Placa, Saldo,
               Resultado, "Cod. Rejeicao", "Mot. Rejeicao",
               TP_SOLICITACAO, SALDO_DIARIO, ID_PEDIDO, WL_LIBERADO
        FROM autorizacoes
    """)
    rows = cursor.fetchall()

    # Obter os nomes das colunas dinamicamente
    colunas = [descricao[0] for descricao in cursor.description]

    nome_arquivo = dt_arqui_nm

    # Caminho do CSV
    caminho_csv = os.path.join(
        pasta_saida, f"{nome_arquivo}.csv")

    with open(caminho_csv, mode="w", newline="", encoding="utf-8") as arquivo_csv: # NOQA
        writer = csv.writer(arquivo_csv, delimiter=",")

        writer.writerow(colunas)  # Escreve o cabeçalho
        writer.writerows(rows)    # Escreve os dados

    cursor.close()
    conexao.close()

    if caminho['RP_ESC_LOG'] == 'Sim':
        msg_log = f'CSV gerado com sucesso com {len(rows)} registros!' # noqa
        log_info(f'Arquivo criado com {len(rows)} registros')


def resetar_tabela_transacoes():
    caminho = caminhos()

    log_info('Iniciando o reset do banco SQL para autorizações!')

    conexao = sqlite3.connect(caminho['BANCOSQLITE'])
    cursor = conexao.cursor()

    try:
        # Apaga todos os registros
        cursor.execute("DELETE FROM autorizacoes;")
        conexao.commit()

        # Compacta o banco (libera espaço)
        cursor.execute("VACUUM;")

        # Reseta o autoincremento (se necessário)
        cursor.execute("""UPDATE sqlite_sequence
                            SET seq = 0
                                WHERE name = 'autorizacoes';""")

        conexao.commit()

        log_info('Banco resetado resetado')

    except Exception as e:
        log_error(f'Erro ao resetar a tabela: {e}')

    finally:
        cursor.close()
        conexao.close()
