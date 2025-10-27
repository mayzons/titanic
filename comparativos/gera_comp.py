from utils.logs_escrita import log_info
from utils.caminhos import caminhos
import sqlite3
from datetime import datetime, timedelta
from comparativos.atualiza_comp import puxa_excel_zero


def data_exec_zero():
    caminho = caminhos()
    log_info('Validando a data de Execução no banco SQL!')

    conexao = sqlite3.connect(caminho['BANCOSQLITE'])
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT MAX(Data)
        FROM execucao
        WHERE frente = 'ZERO TRANSACAO'
    """)
    row = cursor.fetchone()[0]

    cursor.close()
    conexao.close()

    return row


def executa_zero():
    caminho = caminhos()
    data_banco = data_exec_zero()
    agora = datetime.now()

    if data_banco is None:
        log_info('Nenhuma execução anterior encontrada.')
        puxa_excel_zero(caminho['RP_ARQ_ZEROTRN'])
        log_info('Rotina de criação de expurgos concluída!')
        return True

    try:
        # Converte a string salva no banco para datetime
        data_banco = datetime.strptime(data_banco, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        # Caso a data tenha sido salva sem hora
        data_banco = datetime.strptime(data_banco, '%Y-%m-%d')

    diferenca = agora - data_banco

    if diferenca > timedelta(hours=2):
        log_info(f'Última execução há {diferenca.total_seconds() / 3600:.1f} horas. Iniciando nova execução...')  # noqa
        puxa_excel_zero(caminho['RP_ARQ_ZEROTRN'])
        log_info('Rotina de criação de expurgos concluída!')
        return True
    else:
        log_info(f'Última execução há apenas {diferenca.total_seconds() / 3600:.1f} horas. Aguardando 2 horas para nova execução.')  # noqa
        return False
