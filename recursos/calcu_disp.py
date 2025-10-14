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

# Função para converter strings de data/hora em objetos datetime
def converter_data(data):
    return pd.to_datetime(data, format="%d/%m/%Y %H:%M", errors="coerce")  # Evita erro se houver valores inválidos

# 📂 Nome do arquivo de entrada
arquivo_entrada = os.path.join(PASTA_DISP_CALC_ENT, 'Critical.xlsx')

# 📖 Ler o arquivo Excel e remover espaços nos nomes das colunas
df = pd.read_excel(arquivo_entrada, header=0)
df.columns = df.columns.str.strip()  # Remove espaços extras

# 🔍 Verificar se as colunas "Inicio" e "Fim" existem
print("Colunas do DataFrame:", df.columns.tolist())

# 🛠️ Se a coluna "Fim" não existir, pode estar com outro nome. Verifique manualmente.
if "Final" not in df.columns:
    raise ValueError("⚠️ Erro: A coluna 'Fim' não foi encontrada no arquivo. Verifique os nomes das colunas.")

# 📝 Aplicar a conversão
df["Inicio"] = df["Inicio"].apply(converter_data)
df["Final"] = df["Final"].apply(converter_data)

# Função para calcular o tempo total de indisponibilidade sem sobreposição
def calcular_indisponibilidade(grupo):
    eventos = []
    
    for _, row in grupo.iterrows():
        inicio = converter_data(row["Inicio"])
        final = converter_data(row["Final"])
        eventos.append((inicio, final))
    
    # Ordenar eventos pelo início
    eventos.sort()
    
    tempo_total = 0
    inicio_atual, fim_atual = eventos[0]
    
    for inicio, final in eventos[1:]:
        if inicio <= fim_atual:  # Há sobreposição
            fim_atual = max(fim_atual, final)
        else:
            tempo_total += (fim_atual - inicio_atual).total_seconds()
            inicio_atual, fim_atual = inicio, final
    
    # Adiciona o último período
    tempo_total += (fim_atual - inicio_atual).total_seconds()
    
    return tempo_total / 60  # Converte para minutos

# 📂 Nome do arquivo de entrada e saída
arquivo_entrada = os.path.join(PASTA_DISP_CALC_ENT, 'Critical.xlsx')
arquivo_saida = os.path.join(PASTA_DISP_CALC_SAI, 'Critical_ok.xlsx')

# 📖 Ler o arquivo Excel
df = pd.read_excel(arquivo_entrada)

# 📝 Calcular tempo consolidado por Código (ou outra chave única)
# df["Tempo Calculado"] = df.groupby("Código").apply(calcular_indisponibilidade).reset_index(drop=True)
# df["Tempo Calculado"] = df.groupby("Código").apply(calcular_indisponibilidade)
df["Tempo Calculado"] = df.groupby("Código").apply(lambda g: calcular_indisponibilidade(g.drop(columns=["Código"])))

# 🔄 Remover duplicatas mantendo apenas uma linha por grupo
df = df.drop_duplicates(subset=["Código"])

# 💾 Salvar o resultado em um novo arquivo Excel
df.to_excel(arquivo_saida, index=False)

print(f"✅ Processamento concluído! O arquivo '{arquivo_saida}' contém os tempos consolidados.")

# 🚀 Se o erro persistir, poste a saída de `print(df.columns.tolist())` aqui para analisarmos juntos!



# 📊 Exibir o resultado
# if __name__ == "__main__":
    # DEV_DIR_DE = r'C:\\script\\amb_dv\\base\\'
    # DEV_DIR_PARA = r'C:\\script\\amb_dv\\1_tratar'
    # DEV_DIR_DE_DISP = r'C:\\script\\amb_dv\\4_SLA_DETALHADO'
    # DEV_DIR_PARA_DISP = r'C:\\script\\amb_dv\\8_disp_calculo_entrega'

    # if ambiente =='Dev':
    #     os.system(f'copy {DEV_DIR_DE} {DEV_DIR_PARA}')
    #     os.system('cls')
    #     print()
    #     print('Arquivos compiados para paste de testes')
    #     print()
