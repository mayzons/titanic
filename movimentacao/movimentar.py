from movimentacao.definicoes import move_arquivo
from utils.caminhos import caminhos


def movimentacao_arq():
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
