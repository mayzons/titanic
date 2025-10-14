import os
import pandas as pd
from utils.logs_escrita import log_info
from utils.caminhos import caminhos

from pathlib import Path
import shutil


def remover_caminho(caminho_saida: str):
    p = Path(caminho_saida)
    if p.is_file():
        # apaga arquivo
        try:
            p.unlink()
        except FileNotFoundError:
            pass
    elif p.is_dir():
        # apaga pasta (recursivo)
        shutil.rmtree(p, ignore_errors=True)
    else:
        # não existe: nada a fazer
        pass


def consolida_arq(dir_entrada):
    caminho = caminhos()
    # Novos caminhos
    caminho_saida = os.path.join(dir_entrada, "processados")
    arq_saida = os.path.join(dir_entrada, "consolidado.xlsx")
    remover_caminho(caminho_saida)
    os.system(f'del {arq_saida}')  # apaga arquivo se existir
    os.makedirs(caminho_saida, exist_ok=True)

    dfs = []
    contador = 0
    # Percorre todos os arquivos CSV no diretório
    arquivos_pasta = os.listdir(caminho['RP_CONSOLIDACAO'])
    total_arquivos = len(os.listdir(caminho['RP_CONSOLIDACAO']))

    if total_arquivos > 1:
        for arquivo in arquivos_pasta:
            if arquivo.lower() != "consolidado.xlsx":
                caminho_arquivo = os.path.join(dir_entrada, arquivo)
                nome, extensao = os.path.splitext(arquivo)

                # Lê o CSV (separador vírgula)
                if extensao.lower() == ".csv" or extensao.lower() == ".txt":
                    df = pd.read_csv(
                        caminho_arquivo, sep=",", encoding="utf-8")

                # Lê o CSV (separador vírgula)
                elif extensao.lower() == ".xlsx":
                    df = pd.read_excel(caminho_arquivo)

                else:
                    # pula arquivos que não sejam CSV nem XLSX
                    continue

                # (Opcional) adicionar uma coluna para identificar
                df["Arquivo_Origem"] = arquivo

                dfs.append(df)

                # Mover o arquivo para "processados"
                shutil.move(caminho_arquivo, caminho_saida)
                contador += 1

        # Concatena todos os DataFrames em um só
        df_final = pd.concat(dfs, ignore_index=True)

        # Salva em um único arquivo Excel, aba única
        df_final.to_excel(arq_saida, index=False, sheet_name="Unificado")

        log_info('Sem arquivos para processar no consolidador!')
    else:
        log_info(f'O foram processados {contador} arquivos!')
