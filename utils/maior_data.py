import string
import os
from datetime import datetime, timedelta


def definir_data(caminho):
    arquivos_pasta = os.listdir(caminho)
    arquivos_pasta_tr = []

    alf_mai = list(string.ascii_uppercase)
    alf_min = list(string.ascii_lowercase)
    exten = [
        '.csv', '.txt', '.xlsx', '.xlx', '.pdf',
        '.CSV', '.TXT', '.XLSX', '.XLX', '.PDF'
    ]

    caract = [' - ', '?', '!', '/', '*', '#', ',', ' ']

    substituicoes = alf_mai + alf_min + caract

    for arquivo in arquivos_pasta:
        if arquivo == "current.txt":
            continue

        try:
            novo_nome = arquivo
            for j in exten:
                novo_nome = novo_nome.replace(j, '')
            for i in substituicoes:
                novo_nome = novo_nome.replace(i, '')  # ✅ acumula substituições

            novo_nome = novo_nome.replace('.', '_')
            novo_nome = novo_nome.strip()

            conv_data = datetime.strptime(novo_nome, '%d_%m_%Y')
            arquivos_pasta_tr.append(conv_data)  # mantém como datetime
        except ValueError:
            continue

    if not arquivos_pasta_tr:
        # raise ValueError("Nenhum arquivo com data válida encontrado!")
        data_ret = datetime.now() - timedelta(days=2)
        return data_ret

    return max(arquivos_pasta_tr)  # retorna datetime


def verificar_arquivo(caminho_arquivo, h):
    if not os.path.exists(caminho_arquivo):
        return "Sim"
        # raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

    # Pega a data de modificação do arquivo (em segundos desde epoch)
    timestamp_modificacao = os.path.getmtime(caminho_arquivo)
    data_modificacao = datetime.fromtimestamp(timestamp_modificacao)

    # Calcula diferença de tempo
    agora = datetime.now()
    diferenca = agora - data_modificacao

    # Verifica se passou mais de 2 horas
    if diferenca >= timedelta(hours=h):
        return "Sim"
    else:
        return "Não"


def definir_data_menor(caminho):
    arquivos_pasta = os.listdir(caminho)
    arquivos_pasta_tr = []  # lista de tuplas (data, arquivo)

    alf_mai = list(string.ascii_uppercase)
    alf_min = list(string.ascii_lowercase)
    exten = [
        '.csv', '.txt', '.xlsx', '.xlx', '.pdf',
        '.CSV', '.TXT', '.XLSX', '.XLX', '.PDF'
    ]

    caract = [' - ', '?', '!', '/', '*', '#', ',', ' ']

    substituicoes = alf_mai + alf_min + caract

    for arquivo in arquivos_pasta:
        if arquivo == "current.txt":
            continue

        try:
            novo_nome = arquivo
            for j in exten:
                novo_nome = novo_nome.replace(j, '')
            for i in substituicoes:
                novo_nome = novo_nome.replace(i, '')  # ✅acumula substituições

            novo_nome = novo_nome.replace('.', '_')
            novo_nome = novo_nome.strip()
            novo_nome = novo_nome.lstrip('_')  # remove "_" só do início

            conv_data = datetime.strptime(novo_nome, '%d_%m_%Y')
            arquivos_pasta_tr.append((conv_data, arquivo))  # data e nome
        except ValueError:
            continue

    if not arquivos_pasta_tr:
        # raise ValueError("Nenhum arquivo com data válida encontrado!")
        return datetime.now(), None

    # pega a tupla com menor data
    menor_data, menor_arquivo = min(arquivos_pasta_tr, key=lambda x: x[0])
    return menor_data, menor_arquivo
