import os
from autorizacao_max.autorizacao_max import (
    executa, insert_sqlite, exportar_para_csv,
    resetar_tabela_transacoes)
from utils.caminhos import caminhos
from utils.logs_escrita import log_info
from utils.maior_data import verificar_arquivo


def gera_autorizacao_max():
    caminho = caminhos()
    autorizacao = []

    caminho_arquivo = os.path.join(
        caminho['RP_AUTORIZACAO_MAX'], "Autorizacoes_max.txt")
    roda_rotina = verificar_arquivo(caminho_arquivo, 1)

    if roda_rotina == 'Sim':
        resetar_tabela_transacoes()
        autorizacao = executa()
        insert_sqlite(autorizacao)
        exportar_para_csv("Autorizacoes_max", caminho['RP_AUTORIZACAO_MAX'])
    else:
        log_info('A autorização_max rodou a menos de 1 hora!')
