from autorizacao.autorizacao import (
    executa, insert_sqlite, exportar_para_csv, resetar_tabela_transacoes
)
from utils.caminhos import caminhos
from utils.logs_escrita import log_info
from utils.maior_data import definir_data
from datetime import datetime, timedelta


def gera_autorizacao():
    data_inicio: datetime = None  # type: ignore
    data_fim: datetime = None  # type: ignore
    caminho = caminhos()
    maior_data = definir_data(caminho['RP_TRANSACAO']) + timedelta(days=1)

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
        autorizacao = executa(inicio, fim)
        insert_sqlite(autorizacao)
        exportar_para_csv(nm_arquivo, caminho['RP_AUTORIZACAO'])

    else:
        # Automático → pega maior data +1
        if maior_comparacao < data_atual:
            comeco = '00:00:01'
            termino = '23:59:59'

            datausar = maior_data
            inicio = datetime.strptime(
                f"{datausar.strftime('%d/%m/%Y')} {comeco}", '%d/%m/%Y %H:%M:%S'  # NOQA
            )
            fim = datetime.strptime(
                f"{datausar.strftime('%d/%m/%Y')} {termino}", '%d/%m/%Y %H:%M:%S'  # NOQA
            )
            nm_arquivo = f'{datausar.strftime("%d_%m_%Y")}_AUTO'

            resetar_tabela_transacoes()
            autorizacao = executa(inicio, fim)
            insert_sqlite(autorizacao)
            exportar_para_csv(nm_arquivo, caminho['RP_AUTORIZACAO'])

            log_info(f'Autorização gerada para {datausar.date()} com sucesso!')  # NOQA

        else:
            log_info(f'A transação para {maior_data.date()} já foi gerada, nenhuma ação executada.')  # NOQA
