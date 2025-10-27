import os
import pandas as pd
from utils.logs_escrita import log_info
from utils.caminhos import caminhos
from utils.maior_data import definir_data
from datetime import timedelta


def gera_aut_tivit():
    caminho = caminhos()

    log_info('Iniciando a geração de Autorizção Tivit')

    cam_autoriza = caminho['RP_AUTORIZACAO']
    cam_autoriza_tiv = caminho['RP_AUTORIZA_TIVIT']
    data_aut = definir_data(cam_autoriza)
    data_aut_tiv = definir_data(cam_autoriza_tiv)
    data_gerar = data_aut_tiv + timedelta(days=1)
    data_gerar = data_gerar.strftime('%d_%m_%Y')
    nome_autoriza_tivit = os.path.join(
            cam_autoriza_tiv, f'{data_gerar}.csv')

    if data_aut_tiv.date() < data_aut.date():
        resumo = []
        arquivos = os.listdir(cam_autoriza)
        for arquivo in arquivos:
            if f'{data_gerar}.csv' in arquivo.lower():
                df = pd.read_csv(
                    os.path.join(cam_autoriza, arquivo),
                    sep=",", encoding='utf-8')
                colunas_desejadas = ["POSTO", "Data", "Produto"]
                df = df[colunas_desejadas]
                resumo.append(df)

        # ✅ Verificação antes de concatenar
        if not resumo:
            log_info(f"Nenhum arquivo encontrado para a data {data_gerar}. Nenhum CSV gerado.")  # noqa
            return

        df_final = pd.concat(resumo, ignore_index=True)
        df_final.to_csv(nome_autoriza_tivit.replace(".xlsx", ".csv"), index=False, sep=";", encoding="utf-8")  # noqa

        log_info(f"Gerado o arquivo Tivit de autorização: {nome_autoriza_tivit}")  # noqa
