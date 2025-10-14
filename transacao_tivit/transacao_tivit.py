import os
import pandas as pd
from utils.logs_escrita import log_info
from utils.caminhos import caminhos
from utils.maior_data import definir_data
from datetime import timedelta


def gera_tra_tivit():
    caminho = caminhos()

    if caminho['RP_ESC_LOG'] == 'Sim':
        msg_log = f'Iniciando a geração do arquivo Tivit de Transação'  # noqa
        log_info(msg_log)

    cam_transacao = caminho['RP_TRANSACAO']
    cam_transacao_tiv = caminho['RP_TRANSACAO_TIVIT']
    data_aut = definir_data(cam_transacao)
    data_transacao_tiv = definir_data(cam_transacao_tiv)
    data_gerar = data_transacao_tiv + timedelta(days=1)
    data_gerar = data_gerar.strftime('%d_%m_%Y')
    nome_autoriza_tivit = os.path.join(
            cam_transacao_tiv, f'{data_gerar}.txt')

    if data_transacao_tiv.date() < data_aut.date():
        resumo = []
        arquivos = os.listdir(cam_transacao)
        for arquivo in arquivos:
            if arquivo.lower() == f'{data_gerar}.txt':
                nomes_colunas = [
                    "POSTO", "NSU", "TAG",
                    "DATA", "PISTA", "PRODUTO",
                    "TOKEN", "PLACA_CAD", "PLACA_OCR",
                    "CUPOM", "VALOR"
                ]

                df = pd.read_csv(
                    os.path.join(cam_transacao, arquivo),
                    sep="|",
                    header=None,            # <- sem cabeçalho
                    names=nomes_colunas,    # <- define os nomes das colunas
                    encoding="utf-8"
                )

                colunas_desejadas = ["POSTO", "DATA", "TOKEN", "CUPOM"]
                df = df[colunas_desejadas]
                resumo.append(df)

        # Concatena todos os DataFrames em um só
        df_final = pd.concat(resumo, ignore_index=True)

        df_final.to_csv(nome_autoriza_tivit.replace(
            ".xlsx", ".txt"), index=False, sep=",", encoding="utf-8")

        log_info(f'Garado o arquivo Tivit de Transação: {nome_autoriza_tivit}')
