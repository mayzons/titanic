import os
from datetime import datetime
import configparser
from pathlib import Path
import csv
import openpyxl # type: ignore
import pandas as pd # type: ignore
import sys
from openpyxl import Workbook # type: ignore


# Caminho do Parser
def get_app_and_settings_full_path():
    if getattr(sys, 'frozen', False):
        BASE_PATH = os.path.dirname(sys.executable)
    else:
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    print(BASE_PATH)
    return BASE_PATH, os.path.join(BASE_PATH, "Config.ini")
 
CAM_LOGS_LOGS, CAM_CONFIG_PARSER = get_app_and_settings_full_path()

# Criar objeto do configparser
config = configparser.ConfigParser()
with open(CAM_CONFIG_PARSER, "r", encoding="utf-8") as file:
    config.read_file(file)
# Ler o arquivo ini
ambiente = config["ambiente"]["ambiente"]

# Acessar os valores das seções e chaves
LOG_ESCRITA = config[ambiente]["log"]
PASTA_ORIGEM = config[ambiente]["raiz"]
PASTA_DEST_ANTENAS = config[ambiente]['antenas']
PASTA_DEST_SLA = config[ambiente]["sla"]
PASTA_DEST_CRITICAL = config[ambiente]["critical"]
PASTA_DEST_DISPPRO = config[ambiente]["disp_processado"]
PASTA_DEST_DISPPRO_ORIG = config[ambiente]["disp_processado_original"]
PASTA_DISP_CALC_ENT = config[ambiente]["disp_calculo_ent"]
PASTA_DISP_CALC_SAI = config[ambiente]["disp_calculo_sai"]

# Lista para atuação de dados
disp = []
disp_tra = []

#Open excel file
# Função para converter strings de data/hora em objetos datetime
def converter_data(data):
    return pd.to_datetime(data, format="%d/%m/%Y %H:%M", errors="coerce")  # Evita erro se houver valores inválidos

# 📂 Nome do arquivo de entrada
arquivo_entrada = os.path.join(PASTA_DISP_CALC_ENT, 'Critical.xlsx')

# 📖 Ler o arquivo Excel e remover espaços nos nomes das colunas
df = pd.read_excel(arquivo_entrada, header=0)
df.columns = df.columns.str.strip()  # Remove espaços extras



# 📊 Exibir o resultado
if __name__ == "__main__":
    for i in disp:
        data_inicial = datetime.strptime(i[1], "%d/%m/%Y %H:%M:%S")
        data_final = datetime.strptime(i[2], "%d/%m/%Y %H:%M:%S")


        print(i[0], data_inicial, data_final)


