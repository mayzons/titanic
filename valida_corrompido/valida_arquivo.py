import os
import pandas as pd
import openpyxl
import PyPDF2  # type: ignore
import pprint


def validar_arquivos(diretorio):
    corrompidos = []

    for arquivo in os.listdir(diretorio):
        caminho = os.path.join(diretorio, arquivo)

        # Pula pastas
        if not os.path.isfile(caminho):
            continue

        try:
            if arquivo.lower().endswith((".xlsx", ".xls")):
                # Tenta abrir Excel
                wb = openpyxl.load_workbook(caminho, read_only=True)
                wb.close()

            elif arquivo.lower().endswith(".csv"):
                # Tenta ler algumas linhas do CSV
                pd.read_csv(caminho, nrows=5)

            elif arquivo.lower().endswith(".txt"):
                # Apenas tenta abrir e ler
                with open(
                        caminho, "r", encoding="utf-8", errors="strict") as f:
                    f.read(1024)  # lê um pedaço

            elif arquivo.lower().endswith(".pdf"):
                # Tenta abrir PDF
                with open(caminho, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    _ = reader.pages[0]

            else:
                # Se extensão não é suportada, ignora
                continue

        except Exception as e:
            corrompidos.append((f'{diretorio}/{arquivo}', str(e)))

    pprint.pprint(f"Arquivos corrompidos ou inválidos: {corrompidos}")
    # print(f"Arquivos corrompidos ou inválidos: {corrompidos}")

    return corrompidos

cam = r'C:\Users\mayzon.santos\Corpay\Indicadores_PowerBi - Indicadores_PowerBI\WOT_Comparativo'  # noqa


validar_arquivos(cam)
