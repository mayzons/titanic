import pandas as pd
import sqlite3
import os
import shutil
from utils.logs_escrita import log_info
from utils.caminhos import caminhos
import re
from datetime import datetime


def proc_sem_abo(arquivo_csv):
    caminho = caminhos()
    db_path = caminho['BANCOSQLITE_COM']  # caminho do seu banco SQLite

    if not os.path.exists(arquivo_csv):
        log_info(f"Nenhum arquivo para proessar: {arquivo_csv}")
        return

    log_info(f"Lendo arquivo: {arquivo_csv}")

    try:
        # Ler o CSV
        df = pd.read_csv(arquivo_csv, sep=",", encoding="utf-8")
        df.columns = [
            "Codigo_Comp", "Nome", "Data_Report", "Versao",
            "VIP", "Suspenso", "Bandeira", "Disp_Final"
        ]

        # Corrigir possíveis erros de encoding
        df.columns = df.columns.str.replace("Ã³", "ó").str.replace("Ã§", "ç")

        # Tratar os dados
        df["Data_Report"] = pd.to_datetime(
            df["Data_Report"], errors="coerce").dt.date.astype(str)
        df["Disp_Final"] = (
            df["Disp_Final"]
            .astype(str)
            .str.replace("%", "")
            .str.replace(",", ".")
        )
        df["Disp_Final"] = pd.to_numeric(
            df["Disp_Final"], errors="coerce").fillna(0)
        df["Arquivo_Origem"] = os.path.basename(arquivo_csv)

        # Capturar a data do CSV
        data_csv = df["Data_Report"].iloc[0]
        log_info(f"Data encontrada no CSV: {data_csv}")

        # Conectar ao banco
        con = sqlite3.connect(db_path)
        cur = con.cursor()

        # Verificar se a data já existe
        cur.execute("SELECT COUNT(*) FROM DISP_S_ABON WHERE Data_Report = ?",
                    (data_csv,))
        existe = cur.fetchone()[0] > 0

        if existe:
            log_info(f"Registros existentes encontrados para {data_csv}. Removendo...")  # noqa
            cur.execute("DELETE FROM DISP_S_ABON WHERE Data_Report = ?",
                        (data_csv,))
            con.commit()

        # Inserir novos dados
        df.to_sql("DISP_S_ABON", con, if_exists="append", index=False)
        con.commit()
        con.close()

        log_info(f"Importação concluída com sucesso! {len(df)} linhas inseridas para {data_csv}")  # noqa

    except Exception as e:
        log_info(f"Erro ao processar {arquivo_csv}: {e}")

    destino = os.path.join(caminho['RB_COMPARATIVO'], os.path.basename(arquivo_csv))  # noqa
    # Se já existir um arquivo com o mesmo nome, apaga antes de mover
    if os.path.exists(destino):
        os.remove(destino)
        log_info(f"Arquivo existente removido: {destino}")

    # Agora move o arquivo
    shutil.move(arquivo_csv, destino)
    log_info(f"Arquivo {arquivo_csv} movido para {destino}")


def proc_com_abo(arquivo_csv):
    caminho = caminhos()
    db_path = caminho['BANCOSQLITE_COM']  # caminho do seu banco SQLite

    if not os.path.exists(arquivo_csv):
        log_info(f"Nenhum arquivo para proessar: {arquivo_csv}")
        return

    log_info(f"Lendo arquivo: {arquivo_csv}")

    try:
        # Ler o CSV
        df = pd.read_csv(arquivo_csv, sep=",", encoding="utf-8")
        df.columns = [
            "Codigo_Comp", "Nome", "Data_Report", "Versao",
            "VIP", "Suspenso", "Bandeira", "Disp_Final"
        ]

        # Corrigir possíveis erros de encoding
        df.columns = df.columns.str.replace("Ã³", "ó").str.replace("Ã§", "ç")

        # Tratar os dados
        df["Data_Report"] = pd.to_datetime(
            df["Data_Report"], errors="coerce").dt.date.astype(str)
        df["Disp_Final"] = (
            df["Disp_Final"]
            .astype(str)
            .str.replace("%", "")
            .str.replace(",", ".")
        )
        df["Disp_Final"] = pd.to_numeric(
            df["Disp_Final"], errors="coerce").fillna(0)
        df["Arquivo_Origem"] = os.path.basename(arquivo_csv)

        # Capturar a data do CSV
        data_csv = df["Data_Report"].iloc[0]
        log_info(f"Data encontrada no CSV: {data_csv}")

        # Conectar ao banco
        con = sqlite3.connect(db_path)
        cur = con.cursor()

        # Verificar se a data já existe
        cur.execute("SELECT COUNT(*) FROM DISP_C_ABON WHERE Data_Report = ?",
                    (data_csv,))
        existe = cur.fetchone()[0] > 0

        if existe:
            log_info(f"Registros existentes encontrados para {data_csv}. Removendo...")  # noqa
            cur.execute("DELETE FROM DISP_C_ABON WHERE Data_Report = ?",
                        (data_csv,))
            con.commit()

        # Inserir novos dados
        df.to_sql("DISP_S_ABON", con, if_exists="append", index=False)
        con.commit()
        con.close()

        log_info(f"Importação concluída com sucesso! {len(df)} linhas inseridas para {data_csv}")  # noqa

    except Exception as e:
        log_info(f"Erro ao processar {arquivo_csv}: {e}")

    destino = os.path.join(
        caminho['RB_COMPARATIVO'], os.path.basename(arquivo_csv))

    # Se já existir um arquivo com o mesmo nome, apaga antes de mover
    if os.path.exists(destino):
        os.remove(destino)
        log_info(f"Arquivo existente removido: {destino}")

    # Agora move o arquivo
    shutil.move(arquivo_csv, destino)
    log_info(f"Arquivo {arquivo_csv} movido para {destino}")


def proc_opc(arquivo_opc):
    caminho = caminhos()

    try:
        # arquivo_opc = r'C:\script\amb_dv\1_tratar\OPC 27.10.2025.xlsx'

        log_info(f"Lendo arquivo: {arquivo_opc}")
        # Lê todas as abas e concatena
        dados = pd.read_excel(arquivo_opc, sheet_name=None)
        df = pd.concat(dados.values(), ignore_index=True)

        # Extrair a data do nome
        padrao_data = re.search(
            r'(\d{2}\.\d{2}\.\d{4})', os.path.basename(arquivo_opc))
        if padrao_data:
            data_report = datetime.strptime(
                padrao_data.group(1), "%d.%m.%Y").strftime("%Y-%m-%d")
        else:
            data_report = None

        # Renomear colunas para compatibilidade com o banco
        df.columns = [
            "Codigo", "Nome", "VIP", "Versao_Solucao", "Suspenso",
            "Suspended_Date", "Rua", "Cidade", "Estado", "CEP", "OPC",
            "Data_OPC",
            "CNPJ", "Bandeira", "Rede", "Tipo_Servico", "IP", "Classificacao",
            "Longitude", "Latitude", "Qtd_Pistas"
        ]

        # Adiciona colunas extras
        df["Data_Report"] = data_report
        df["Arquivo_Origem"] = os.path.basename(arquivo_opc)

    # Conectar e garantir tabela
        banco = caminho["BANCOSQLITE_COM"]
        con = sqlite3.connect(banco)
        cur = con.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS REPORT_OPC (
            Codigo TEXT, Nome TEXT, VIP TEXT, Versao_Solucao TEXT,
                    Suspenso TEXT,
            Suspended_Date TEXT, Rua TEXT, Cidade TEXT, Estado TEXT, CEP TEXT,
            OPC TEXT, Data_OPC TEXT, CNPJ TEXT, Bandeira TEXT, Rede TEXT,
            Tipo_Servico TEXT, IP TEXT, Classificacao TEXT, Longitude TEXT,
            Latitude TEXT, Qtd_Pistas TEXT, Data_Report TEXT,
            Arquivo_Origem TEXT
        )
        """)
        con.commit()

        # Remover registros da data já existente
        cur.execute("DELETE FROM REPORT_OPC WHERE Data_Report = ?",
                    (data_report,))
        con.commit()

        # Inserir dados limpos
        df.to_sql("REPORT_OPC", con, if_exists="append", index=False)
        con.commit()
        con.close()

        log_info(f"{len(df)} registros processados para {data_report}")
        os.remove(arquivo_opc)

    except Exception as e:
        log_info(f"Erro ao processar {arquivo_opc}: {e}")


def puxa_excel_zero(arquivo_excel):
    hoje = datetime.now()
    hoje_date = datetime.now().date()
    hora_atual_str = hoje.strftime("%H:%M:%S")

    caminho = caminhos()
    # Caminho do Excel e do banco SQLite
    banco_sqlite = caminho['BANCOSQLITE_COM']  # noqa

    # Nome da aba no Excel
    aba = "Zero"

    colunas_desejadas = [
        "Data Report", "Código", "Nome", "Vip", "Data TRNX", "Dias s\\ TRNX",
        "Status", "Grupo", "Total de TRN 2024", "Média TRN x Mês",
        "SLA Violado", "% SLA", "Chamado", "Grupo designado",
        "Criado em:", "IP", "Versão da Solução", "Rede", "Tipo de Serviço",
        "Cidade", "Estado"
    ]

    df = pd.read_excel(arquivo_excel, sheet_name=aba, usecols=colunas_desejadas)  # noqa

    # Renomear colunas para compatibilidade com o banco
    df.columns = [
        "Data_Report", "Codigo", "Nome", "VIP", "Data_TRNX", "Dias_s_TRNX",
        "Status", "Grupo", "Total_TRN_2024", "Media_TRN_Mes",
        "SLA_Violado", "Perc_SLA", "Chamado", "Grupo_Designado",
        "Criado_em", "IP", "Versao_Solucao", "Rede",
        "Tipo_Servico", "Cidade", "Estado"
    ]

    # Converter Data_Report para apenas data (YYYY-MM-DD)
    df["Data_Report"] = pd.to_datetime(df["Data_Report"]).dt.date.astype(str)

    # Converter % SLA para float
    df["Perc_SLA"] = (
        df["Perc_SLA"]
        .astype(str)
        .str.replace("%", "")
        .str.replace(",", ".")
    )
    df["Perc_SLA"] = pd.to_numeric(df["Perc_SLA"], errors="coerce")

    # Conectar ao SQLite
    con = sqlite3.connect(banco_sqlite)
    cursor = con.cursor()

    # Criar tabela (caso não exista)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ZERO_TRN (
        Data_Report TEXT, Codigo TEXT, Nome TEXT, VIP TEXT, Data_TRNX TEXT,
        Dias_s_TRNX INTEGER, Status TEXT, Grupo TEXT, Total_TRN_2024 INTEGER,
        Media_TRN_Mes INTEGER, SLA_Violado TEXT, Perc_SLA REAL, Chamado TEXT,
        Grupo_Designado TEXT, Criado_em TEXT, IP TEXT, Versao_Solucao TEXT,
        Rede TEXT, Tipo_Servico TEXT, Cidade TEXT, Estado TEXT
    )
    """)

    # Verificar se já existe a Data_Report no banco
    data_relatorio = df["Data_Report"].iloc[0]
    cursor.execute("SELECT COUNT(*) FROM ZERO_TRN WHERE Data_Report = ?",
                   (data_relatorio,))
    existe = cursor.fetchone()[0]

    if existe > 0:
        print(f"Já existe registro para Data_Report = {data_relatorio}. Nenhuma linha inserida.") # noqa
    else:
        log_info(f"Inserindo {len(df)} registros do Zero para Data_Report = {data_relatorio}...") # noqa
        df.to_sql("ZERO_TRN", con, if_exists="append", index=False)
        con.commit()
        insert_sqlite([('ZERO TRANSACAO', hoje_date,
                        hora_atual_str, 'automatica')])

    con.close()


def puxa_excel_disp_sem():
    caminho = caminhos()
    print("COMECANDO DISP SEM")
    # Caminho do Excel e do banco SQLite
    arquivo_excel = r"C:\\Users\\mayzon.santos\\OneDrive - Corpay\\Documents\\Outras frentes\\Ações Ricardo\\Comparativos\\Comp. Bases (Disp vs Zero).xlsx"  # noqa
    banco_sqlite = caminho['BANCOSQLITE_COM'] # noqa

    # Nome da aba no Excel
    aba = "Disp_Sem"

    colunas_desejadas = [
        "Código Comp.", "Nome", "Data Report", "Versão", "VIP",
        "Suspenso", "Bandeira", "Disp. Final]", "Arquivo_Origem"
    ]

    print("📂 Lendo Excel...")
    df = pd.read_excel(
        arquivo_excel, sheet_name=aba, usecols=colunas_desejadas)

    # Renomear colunas para compatibilidade com o banco
    df.columns = [
        "Codigo_Comp", "Nome", "Data_Report", "Versao", "VIP",
        "Suspenso", "Bandeira", "Disp_Final", "Arquivo_Origem"
    ]

    # Limpar os dados
    df["Disp_Final"] = (
        df["Disp_Final"]
        .astype(str)
        .str.replace("%", "")
        .str.replace(",", ".")
        .astype(float)
    )

    # Converter Data_Report para apenas data (YYYY-MM-DD)
    df["Data_Report"] = pd.to_datetime(df["Data_Report"]).dt.date.astype(str)

    # Conectar ao banco SQLite
    con = sqlite3.connect(banco_sqlite)
    cursor = con.cursor()

    # Criar tabela se não existir
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DISP_S_ABON (
        Codigo_Comp TEXT, Nome TEXT, Data_Report TEXT, Versao TEXT,
        VIP TEXT, Suspenso TEXT, Bandeira TEXT, Disp_Final REAL,
        Arquivo_Origem TEXT
    )
    """)

    # Verificar se já existe a Data_Report no banco
    data_relatorio = df["Data_Report"].iloc[0]
    cursor.execute("SELECT COUNT(*) FROM DISP_S_ABON WHERE Data_Report = ?",
                   (data_relatorio,))
    existe = cursor.fetchone()[0]

    if existe > 0:
        print(f"🗑️  Removendo registros antigos para Data_Report = {data_relatorio}...")  # noqa
        cursor.execute("DELETE FROM DISP_S_ABON WHERE Data_Report = ?", (data_relatorio,))  # noqa
        con.commit()

    # Inserir os dados novos
    print(f"💾 Gravando {len(df)} linhas no SQLite...")
    df.to_sql("DISP_S_ABON", con, if_exists="append", index=False)

    # Confirmar e fechar
    con.commit()
    con.close()

    print(f"✅ Importação concluída com sucesso! {len(df)} linhas inseridas para {data_relatorio}.")  # noqa


def puxa_excel_disp_com():
    caminho = caminhos()
    print("COMECANDO DISP COM")
    # Caminho do Excel e do banco SQLite
    arquivo_excel = r"C:\\Users\\mayzon.santos\\OneDrive - Corpay\\Documents\\Outras frentes\\Ações Ricardo\\Comparativos\\Comp. Bases (Disp vs Zero).xlsx"  # noqa
    banco_sqlite = caminho['BANCOSQLITE_COM']  # noqa

    # Nome da aba no Excel
    aba = "Disp"

    colunas_desejadas = [
        "Código Comp.", "Nome", "Data Report", "Versão", "VIP",
        "Suspenso", "Bandeira", "Disp. Final]", "Arquivo_Origem"
    ]

    print("📂 Lendo Excel disp com...")
    df = pd.read_excel(
        arquivo_excel, sheet_name=aba, usecols=colunas_desejadas)

    # Renomear colunas para compatibilidade com o banco
    df.columns = [
        "Codigo_Comp", "Nome", "Data_Report", "Versao", "VIP",
        "Suspenso", "Bandeira", "Disp_Final", "Arquivo_Origem"
    ]

    # Limpar os dados
    df["Disp_Final"] = (
        df["Disp_Final"]
        .astype(str)
        .str.replace("%", "")
        .str.replace(",", ".")
        .astype(float)
    )

    # Converter Data_Report para apenas data (YYYY-MM-DD)
    df["Data_Report"] = pd.to_datetime(df["Data_Report"]).dt.date.astype(str)

    # Conectar ao banco SQLite
    con = sqlite3.connect(banco_sqlite)
    cursor = con.cursor()

    # Criar tabela se não existir
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DISP_C_ABON (
        Codigo_Comp TEXT, Nome TEXT, Data_Report TEXT, Versao TEXT,
        VIP TEXT, Suspenso TEXT, Bandeira TEXT, Disp_Final REAL,
        Arquivo_Origem TEXT
    )
    """)

    # Verificar se já existe a Data_Report no banco
    data_relatorio = df["Data_Report"].iloc[0]
    cursor.execute("SELECT COUNT(*) FROM DISP_C_ABON WHERE Data_Report = ?",
                   (data_relatorio,))
    existe = cursor.fetchone()[0]

    if existe > 0:
        print(f"🗑️  Removendo registros antigos para Data_Report = {data_relatorio}...")  # noqa
        cursor.execute("DELETE FROM DISP_C_ABON WHERE Data_Report = ?", (data_relatorio,))  # noqa
        con.commit()

    # Inserir os dados novos
    print(f"💾 Gravando {len(df)} linhas no SQLite...")
    df.to_sql("DISP_C_ABON", con, if_exists="append", index=False)

    # Confirmar e fechar
    con.commit()
    con.close()

    print(f"✅ Importação concluída com sucesso! {len(df)} linhas inseridas para {data_relatorio}.")  # noqa


def insert_sqlite(exec):
    caminho = caminhos()
    # Criar conexão do SQLite
    log_info('Iniciado a Insersão no banco de dados SQL!')

    connsqlite = sqlite3.connect(caminho['BANCOSQLITE'])
    cursorsqlite = connsqlite.cursor()

    cursorsqlite.execute("""
        CREATE TABLE IF NOT EXISTS execucao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            frente TEXT, Data TEXT, Hora, forma
        );
        """)

    insert_query = """
        INSERT INTO execucao (
            frente, Data, Hora, forma
        ) VALUES (?, ?, ?, ?)
        """

    cursorsqlite.executemany(insert_query, exec)
    connsqlite.commit()
    connsqlite.close()

    log_info(f'Execução {exec} inserida no SQLite com sucesso!')
