import os
from autorizacao_max.autorizacao_max import (
    executa, insert_sqlite, exportar_para_csv,
    resetar_tabela_transacoes)
from utils.caminhos import caminhos
from utils.logs_escrita import log_info
from utils.maior_data import verificar_arquivo


def gera_transacao_max():
    caminho = caminhos()
    transacoes = []

    caminho_arquivo = os.path.join(
        caminho['RP_TRANSACAO_MAX'], "Transacoes_max.txt")
    roda_rotina = verificar_arquivo(caminho_arquivo, 1)

    if roda_rotina == 'Sim':
        resetar_tabela_transacoes()
        transacoes = executa()
        insert_sqlite(transacoes)
        exportar_para_csv("Transacoes_max", caminho['RP_TRANSACAO_MAX'])
    else:
        log_info('A transacao_max rodou a menos de 1 hora!')
