import os
import pandas as pd
from utils.logs_escrita import log_info
from utils.caminhos import caminhos
from utils.maior_data import definir_data
from datetime import timedelta


def gera_tra_tivit():
    caminho = caminhos()

    if caminho['RP_ESC_LOG'] == 'Sim':
        log_info('Iniciando a geração do arquivo Tivit de Transação')

    cam_transacao = caminho['RP_TRANSACAO']
    cam_transacao_tiv = caminho['RP_TRANSACAO_TIVIT']

    # Garante que o diretório de saída exista
    os.makedirs(cam_transacao_tiv, exist_ok=True)

    # Define as datas
    data_aut = definir_data(cam_transacao)
    data_transacao_tiv = definir_data(cam_transacao_tiv)
    data_gerar = data_transacao_tiv + timedelta(days=1)
    data_gerar_fmt = data_gerar.strftime('%d_%m_%Y')
    nome_autoriza_tivit = os.path.join(cam_transacao_tiv, f'{data_gerar_fmt}.txt')  # noqa

    # Só gera se houver transações mais recentes
    if data_transacao_tiv.date() < data_aut.date():
        resumo = []
        arquivos = os.listdir(cam_transacao)

        log_info(f'Procurando arquivos em {cam_transacao} para a data {data_gerar_fmt}...')  # noqa

        # Verifica se o arquivo do dia existe
        encontrou = False
        for arquivo in arquivos:
            if arquivo.lower() == f'{data_gerar_fmt}.txt':
                encontrou = True
                caminho_arquivo = os.path.join(cam_transacao, arquivo)

                log_info(f'Lendo arquivo: {caminho_arquivo}')

                nomes_colunas = [
                    "POSTO", "NSU", "TAG",
                    "DATA", "PISTA", "PRODUTO",
                    "TOKEN", "PLACA_CAD", "PLACA_OCR",
                    "CUPOM", "VALOR"
                ]

                try:
                    df = pd.read_csv(
                        caminho_arquivo,
                        sep="|",
                        header=None,
                        names=nomes_colunas,
                        encoding="utf-8"
                    )

                    colunas_desejadas = ["POSTO", "DATA", "TOKEN", "CUPOM"]
                    df = df[colunas_desejadas]
                    resumo.append(df)

                except Exception as e:
                    log_info(f'Erro ao ler {arquivo}: {e}')

        if not encontrou:
            log_info(f'Nenhum arquivo encontrado com o nome {data_gerar_fmt}.txt em {cam_transacao}')  # noqa
            return

        # Evita erro se não houver dados
        if not resumo:
            log_info('Nenhum dado válido encontrado para concatenar.')
            return

        # Concatena os dados
        df_final = pd.concat(resumo, ignore_index=True)

        # Salva o resultado
        df_final.to_csv(nome_autoriza_tivit, index=False, sep=",", encoding="utf-8")  # noqa
        log_info(f'Gerado o arquivo Tivit de Transação: {nome_autoriza_tivit}')

    else:
        log_info('Nenhum novo arquivo a ser gerado. As datas estão sincronizadas.')  # noqa
