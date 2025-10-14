from exp_autorizacao.exp_autor import (
    executa, insert_sqlite, abrir_arquivo_crit,
    resetar_tabela_transacoes)
from utils.maior_data import definir_data
from utils.caminhos import caminhos
from utils.logs_escrita import log_info
from datetime import datetime, timedelta


def gera_expu_autorizacao():
    caminho = caminhos()

    maior_data_abon = definir_data(caminho['RP_AUTORIZA_ABONO'])
    maior_data_crit = definir_data(caminho['RP_D_CRITICAL'])

    maior_data_abon_ger = maior_data_abon + timedelta(days=1)

    maior_comparacao_abon = maior_data_abon.date()
    maior_comparacao_crit = maior_data_crit.date()

    if maior_comparacao_abon < maior_comparacao_crit:
        comeco = '08:00:00'
        termino = '17:59:00'
        datausar = maior_data_abon_ger
        inicio = datetime.strptime(
            f"{datausar.strftime('%d/%m/%Y')} {comeco}", '%d/%m/%Y %H:%M:%S')
        fim = datetime.strptime(
            f"{datausar.strftime('%d/%m/%Y')} {termino}", '%d/%m/%Y %H:%M:%S')

        expu_autorizacao = executa(inicio, fim)
        resetar_tabela_transacoes()
        insert_sqlite(expu_autorizacao)
        abrir_arquivo_crit(maior_data_abon_ger)

    else:
        log_info(f'O expurgo de autorização para {maior_comparacao_abon} já foi gerada!')  # noqa
