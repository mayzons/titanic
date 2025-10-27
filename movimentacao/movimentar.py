from movimentacao.definicoes import move_arquivo
from utils.caminhos import caminhos
from utils.logs_escrita import log_info
import inspect


def movimentacao_arq():

    caller = inspect.stack()[1]  # [0] é a própria função
    msg = f"Função chamada por: {caller.function} (arquivo: {caller.filename}, linha {caller.lineno})"  # noqa
    print(msg)
    log_info('Iniciando o reset do banco SQL para autorizações!')

    caminho = caminhos()

    # Mover OPC Disponibilidade
    move_arquivo(
        caminho['RP_D_OPC'],
        caminho['RB_D_OPC'],
        caminho['RP_DIAS_EXP'])

    # Mover Critical Disponibilidade
    move_arquivo(
        caminho['RP_D_CRITICAL'],
        caminho['RB_CRITICAL'],
        caminho['RP_DIAS_EXP'])

    # # Mover Transacao
    move_arquivo(
        caminho['RP_TRANSACAO'],
        caminho['RB_TRANSACAO'],
        caminho['RP_DIAS_EXP'])

    # # Mover Autorizacao
    move_arquivo(
        caminho['RP_AUTORIZA_ABONO'],
        caminho['RB_AUTORIZA_ABONO'],
        caminho['RP_DIAS_EXP'])
