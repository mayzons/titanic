import os
from utils.logs_escrita import log_info, log_error, log_critical
from utils.caminhos import caminhos
from disponibilidade.definicoes import nome_col, apaga_linha, gera_disp
from comparativos.atualiza_comp import proc_com_abo, proc_sem_abo


def executar_limpeza(caminho):
    # Carregar os caminhos do arquivo de configuração
    caminho = caminhos()

    total_arquivos = int(
        len([arquivo for arquivo in os.listdir(caminho['RP_RAIZ'])]))

    while total_arquivos > 0:
        # Lista todos os arquivos na pasta de origem
        arquivos_para_processar = [
            arquivo for arquivo in os.listdir(caminho['RP_RAIZ'])
            ]

        if arquivos_para_processar:
            for arquivo in arquivos_para_processar:
                # Caminho completo do arquivo
                arquivo_origem = os.path.join(
                    caminho['RP_RAIZ'], arquivo)
                try:
                    # Processar o arquivo encontrado
                    if 'critical' in arquivo.lower():
                        nome_col(
                            arquivo_origem, caminho['RP_RAIZ'], arquivo)

                        total_arquivos -= 1

                    elif 'sla_abastece' in arquivo.lower():
                        apaga_linha(
                            arquivo_origem, caminho['RP_RAIZ'], arquivo)

                        total_arquivos -= 1

                    elif 'a_antena_geral' in arquivo.lower():
                        apaga_linha(
                            arquivo_origem, caminho['RP_RAIZ'], arquivo)
                        total_arquivos -= 1

                    elif 'disp_processada' in arquivo.lower():
                        gera_disp(
                            arquivo_origem, caminho['RP_RAIZ'], arquivo)

                        total_arquivos -= 1

                    elif 'disp_sem_abono' in arquivo.lower():
                        proc_sem_abo(
                            arquivo_origem)

                        total_arquivos -= 1

                    elif 'disp_com_abono' in arquivo.lower():
                        proc_com_abo(
                            arquivo_origem)

                        total_arquivos -= 1

                    elif 'opc ' in arquivo.lower():
                        proc_com_abo(
                            arquivo_origem)

                        total_arquivos -= 1

                    else:
                        log_info(f'O arquivo {arquivo} foi apagado')
                        os.remove(arquivo_origem)
                        total_arquivos -= 1

                except Exception as e:
                    total_arquivos -= 1
                    log_critical(f'Erro ao processar o arquivo {arquivo_origem}: {e}')  # noqa

        else:
            total_arquivos -= 1
            log_error(f'Erro ao processar o arquivo os arquivos da pasta {caminho['RP_RAIZ']}')  # noqa
