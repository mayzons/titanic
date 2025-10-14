from transacoes.transacao import (
    executa, insert_sqlite, exportar_para_csv,
    resetar_tabela_transacoes)
from utils.caminhos import caminhos
from utils.logs_escrita import log_info
from utils.maior_data import definir_data, verificar_arquivo
import os

from datetime import datetime, timedelta


def gera_transacao(
        data_inicio: datetime = None,  # type: ignore
        data_fim: datetime = None,  # type: ignore
        saida: str = None):  # type: ignore
    caminho = caminhos()
    maior_data = definir_data(caminho['RP_TRANSACAO']) + timedelta(days=1)
    caminho_current = os.path.join(caminho['RP_TRANSACAO'], "current.txt")
    roda_current = verificar_arquivo(caminho_current, 2)

    data_atual = datetime.now().date()
    maior_comparacao = maior_data.date()

    # =====================================================
    # 🚀 Parte 1: Convencional (Automático / Manual)
    # =====================================================
    if data_inicio and data_fim:
        # Modo manual → usa parâmetros
        inicio = datetime.strptime(
            f"{data_inicio.strftime('%d/%m/%Y')} 00:00:01", '%d/%m/%Y %H:%M:%S'
        )
        fim = datetime.strptime(
            f"{data_fim.strftime('%d/%m/%Y')} 23:59:59", '%d/%m/%Y %H:%M:%S'
        )
        nm_arquivo = f'{data_inicio.strftime("%d_%m_%Y")}_MANUAL'

        resetar_tabela_transacoes()
        transacoes = executa(inicio, fim)
        insert_sqlite(transacoes)
        exportar_para_csv(nm_arquivo, saida)

    else:
        # Automático → pega maior data +1
        if maior_comparacao < data_atual:
            roda_current = 'Não'
            comeco = '00:00:01'
            termino = '23:59:59'

            datausar = maior_data
            inicio = datetime.strptime(
                f"{datausar.strftime('%d/%m/%Y')} {comeco}", '%d/%m/%Y %H:%M:%S'  # NOQA
            )
            fim = datetime.strptime(
                f"{datausar.strftime('%d/%m/%Y')} {termino}", '%d/%m/%Y %H:%M:%S'  # NOQA
            )

            nm_arquivo = f'{datausar.strftime("%d_%m_%Y")}'

            resetar_tabela_transacoes()
            transacoes = executa(inicio, fim)
            insert_sqlite(transacoes)
            exportar_para_csv(nm_arquivo, caminho['RP_TRANSACAO'])
        else:
            if caminho['RP_ESC_LOG'] == 'Sim':
                msg_log = f'A transação para {maior_data.date()} já foi gerada!'  # NOQA
                log_info(msg_log)

    # =====================================================
    # ⚡ Parte 2: Current (mantida separada)
    # =====================================================
    if roda_current == 'Sim':
        comeco = '00:00:01'
        termino = '23:59:59'

        datausar = datetime.now().date()
        inicio = datetime.strptime(
            f"{datausar.strftime('%d/%m/%Y')} {comeco}", '%d/%m/%Y %H:%M:%S'
        )
        fim = datetime.strptime(
            f"{datausar.strftime('%d/%m/%Y')} {termino}", '%d/%m/%Y %H:%M:%S'
        )

        resetar_tabela_transacoes()
        transacoes = executa(inicio, fim)
        insert_sqlite(transacoes)
        exportar_para_csv('current', caminho['RP_TRANSACAO'])
    else:
        if caminho['RP_ESC_LOG'] == 'Sim':
            msg_log = f'Current desativado em {data_atual}'
            log_info(msg_log)


data_inicio = datetime(2025, 9, 1)
data_fim = datetime(2025, 9, 1)
caminho = caminhos()
