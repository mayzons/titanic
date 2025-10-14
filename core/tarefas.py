import os
from utils.caminhos import caminhos
from utils.logs_escrita import log_info
from disponibilidade.limpa_arquivos import executar_limpeza
from autorizacao.gera_autorizacao import gera_autorizacao
from exp_autorizacao.gera_exp_auto import gera_expu_autorizacao
from trn_domingo.gera_trndomin import dia_da_semana
from consolida.consolida import consolida_arq
from autorizacao_tivit.autoriza_tivit import gera_aut_tivit
from transacoes.gera_transacao import gera_transacao
from transacao_tivit.transacao_tivit import gera_tra_tivit
from transacao_max.gera_transacao_max import gera_transacao_max
from autorizacao_max.gera_autorizacao_max import gera_autorizacao_max
from movimentacao.movimentar import movimentacao_arq


def valida_ambiente(caminho):
    # Quando em ambiente de DEV copiar os logs de consumo para teste
    DE_RAIZ = r'C:\\script\\amb_dv\\base\\raiz'
    PARA_RAIZ = r'C:\\script\\amb_dv\\1_tratar'
    if caminho['AMBIENTE'] == 'Dev':
        os.system(f'copy {DE_RAIZ} {PARA_RAIZ}')


def executar_automacao():
    caminho = caminhos()
    if caminho["P_TOTAL"] == "Nao":

        if caminho["AMBIENTE"] == "Dev":
            log_info('#-# Carregamento do ambiente de teste!')
            valida_ambiente(caminho)
            log_info('Fim da cargado do ambiente de teste!')

        log_info("#-# Executando automação automática...")

        if caminho["P_TOTAL"] == "Nao":
            log_info("#-# Verificando pasta base do projeto...")
            executar_limpeza(caminho)
            log_info("#- Termino da rotina da pasta base do projeto!")
        else:
            log_info("Parada ativada, pulando rotina de limpeza!")

        if caminho["P_TOTAL"] == "Nao":
            log_info("#-# Iniciando a geração dos dados de autorizações...")  # noqa
            gera_autorizacao()
            log_info("#- Termino da geração do arquivo de autorizações!")
        else:
            log_info("Parada ativada, pulando rotina de autorizações!")

        if caminho["P_TOTAL"] == "Nao":
            log_info("#-# Iniciando a geração dos dados de expurgo de autorizações...")  # noqa
            gera_expu_autorizacao()
            log_info("#- Termino da geração do arquivo de expurgo de autorizações!")  # noqa
        else:
            log_info("Parada ativada, pulando rotina de expurgo de autorizações!")  # noqa

        if caminho["P_TOTAL"] == "Nao":
            log_info("#-# Iniciando a geração dos dados de autorizações Tivit...")  # noqa
            gera_aut_tivit()
            log_info("#- Termino da geração do arquivo de autorizações Tivit!")
        else:
            log_info("Parada ativada, pulando rotina de autorizações Tivit!")

        if caminho["P_TOTAL"] == "Nao":
            log_info("#-# Iniciando a geração dos dados de autorizações Max...")  # noqa
            gera_autorizacao_max()
            log_info("#- Termino da geração do arquivo de autorizações Max!")
        else:
            log_info("Parada ativada, pulando rotina de autorizações Max!")

        if caminho["P_TOTAL"] == "Nao":
            log_info("#-# Iniciando a geração dos dados de expurgo de domingo...")  # noqa
            dia_da_semana()
            log_info("#- Termino da geração do arquivo de expurgo de domingo!")
        else:
            log_info("Parada ativada, pulando rotina de expurgo de domingo!")

        if caminho["P_TOTAL"] == "Nao":
            log_info("#-# Iniciando a rotina de consolidação de arquivos...")  # noqa
            consolida_arq(caminho['RP_CONSOLIDACAO'])
            log_info("#- Termino da rotina de consolidação de arqquivos!")
        else:
            log_info("Parada ativada, pulando rotina de consolidação de arquivos!")  # noqa

        if caminho["P_TOTAL"] == "Nao":
            log_info("#-# Iniciando a geração dos dados de Transações...")  # noqa
            gera_transacao()
            log_info("#- Termino da geração do arquivo de Transações!")
        else:
            log_info("Parada ativada, pulando rotina de Transações!")

        if caminho["P_TOTAL"] == "Nao":
            log_info("#-# Iniciando a geração dos dados de Transações Tivit...")  # noqa
            gera_tra_tivit()
            log_info("#- Termino da geração do arquivo de Transações Tivit!")
        else:
            log_info("Parada ativada, pulando rotina de Transações Tivit!")

        if caminho["P_TOTAL"] == "Nao":
            log_info("#-# Iniciando a geração dos dados de Transações Max...")  # noqa
            gera_transacao_max()
            log_info("#- Termino da geração do arquivo de Transações Max!")
        else:
            log_info("Parada ativada, pulando rotina de Transações Max!")

        if caminho["P_TOTAL"] == "Nao":
            log_info("#-# Iniciando a rotina de BKP de arquivos...")
            movimentacao_arq()
            log_info("#- Termino da rotina de BKP de arquivos!")
        else:
            log_info("Parada ativada, pulando rotina de BKP de arquivos!")

        log_info("#-# Automação automática concluída com sucesso!")

    else:
        log_info('Execução desativada!')
    return "Automação concluída com sucesso!"
