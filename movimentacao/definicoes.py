import os
import shutil
import string
from datetime import datetime, timedelta

from utils.caminhos import caminhos

try:
    from utils.logs_escrita import log_info    # type: ignore # noqa
except Exception:
    def log_info(msg):
        print("[LOG_INFO]", msg)


def definir_data_menor(caminho):
    """
    Retorna a menor data e arquivo válido na pasta.
    """
    try:
        arquivos_pasta = os.listdir(caminho)
    except Exception:
        return datetime.now(), None

    arquivos_pasta_tr = []

    alf_mai = list(string.ascii_uppercase)
    alf_min = list(string.ascii_lowercase)
    exten = ['.csv', '.txt', '.xlsx', '.xlx', '.pdf',
             '.CSV', '.TXT', '.XLSX', '.XLX', '.PDF']
    caract = [' - ', '?', '!', '/', '*', '#', ',', ' ']
    substituicoes = alf_mai + alf_min + caract

    for arquivo in arquivos_pasta:
        full = os.path.join(caminho, arquivo)
        if not os.path.isfile(full) or arquivo == "current.txt":
            continue
        try:
            novo_nome = arquivo
            for j in exten:
                novo_nome = novo_nome.replace(j, '')
            for i in substituicoes:
                novo_nome = novo_nome.replace(i, '')
            novo_nome = novo_nome.replace('.', '_').strip().lstrip('_')
            conv_data = datetime.strptime(novo_nome, '%d_%m_%Y')
            arquivos_pasta_tr.append((conv_data, arquivo))
        except ValueError:
            continue

    if not arquivos_pasta_tr:
        return datetime.now(), None

    menor_data, menor_arquivo = min(arquivos_pasta_tr, key=lambda x: x[0])
    return menor_data, menor_arquivo


def move_arquivo(entrada, saida, dias, sleep_after_move=0.1):
    """
    Move arquivos da pasta 'entrada' para 'saida' antigos que 'dias'.
    Evita loop infinito e mantém menor_data para uso posterior.
    """
    caminho = caminhos()
    data_corte = datetime.now() - timedelta(days=int(dias))

    entrada = os.path.abspath(entrada)
    saida = os.path.abspath(saida)

    if entrada == saida:
        return  # não mover para mesma pasta

    processed = set()

    while True:
        menor_data, menor_arquivo = definir_data_menor(entrada)

        if menor_arquivo is None:

            log_info(f'Não arquivos para movimentar em {entrada}!')
            break  # não há mais arquivos válidos

        if menor_arquivo in processed:
            break  # já processamos este arquivo nesta execução

        if menor_data < data_corte:
            origem = os.path.join(entrada, menor_arquivo)
            destino = os.path.join(saida, menor_arquivo)

            if not os.path.exists(origem):
                processed.add(menor_arquivo)
                continue

            try:
                os.makedirs(saida, exist_ok=True)
                shutil.move(origem, destino)

                if caminho.get('RP_ESC_LOG') == 'Sim':
                    log_info(
                        f'Arquivo {menor_arquivo} movido para pasta de backup | '  # noqa
                        f'Data do arquivo: {menor_data.strftime("%d/%m/%Y")} | '  # noqa
                        f'Data corte: {data_corte.strftime("%d/%m/%Y")}'
                    )

                processed.add(menor_arquivo)

                # dá tempo para o SO atualizar locks
                import time; time.sleep(sleep_after_move)  # type: ignore # noqa

            except Exception:
                break  # se der erro, aborta para não travar o loop
        else:
            break  # arquivos restantes são novos, sai do loop

    return
