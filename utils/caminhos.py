import os
import json
from datetime import datetime
from config import _RAIZ_PROJETO

_config_cache = None


def _get_config_path():
    """Retorna o caminho absoluto do arquivo config.json"""
    return os.path.join(_RAIZ_PROJETO, "utils", "config.json")


def caminhos(ambiente_escolhido=None):
    """
    Carrega as configurações do ambiente (Dev, Prod etc.) diretamente do JSON.
    Usa cache para evitar reabertura repetida do arquivo.
    """
    global _config_cache
    if _config_cache is not None and ambiente_escolhido is None:
        return _config_cache

    config_path = _get_config_path()

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"⚠️ Arquivo de configuração não encontrado: {config_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"⚠️ Erro ao ler o JSON de configuração: {e}")

    ambiente = ambiente_escolhido or data.get("ambiente") or "Prod"

    if ambiente not in data:
        raise ValueError(
            f"⚠️ Ambiente '{ambiente}' não encontrado no config.json")

    cfg = data[ambiente]

    LOGS = os.path.join(_RAIZ_PROJETO, "logs")
    NM_LOG = datetime.now().strftime("%Y-%m-%d") + ".log"
    os.makedirs(LOGS, exist_ok=True)

    _config_cache = {
        "MINHA_RAIZ": _RAIZ_PROJETO,
        "AMBIENTE": ambiente,
        "LOGS": LOGS,
        "NM_LOG": NM_LOG,
        **cfg,
    }

    return _config_cache


def salvar_caminho(ambiente, dados: dict):
    """
    Atualiza ou insere chaves/valores no config.json
    dentro do ambiente especificado (Dev, Prod etc.)
    """
    if not ambiente or not dados:
        raise ValueError("Ambiente e dados devem ser fornecidos")

    config_path = _get_config_path()

    # Lê o conteúdo atual do JSON
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"ambiente": ambiente, ambiente: {}}

    # Garante que o ambiente existe
    if ambiente not in data:
        data[ambiente] = {}

    # Atualiza os valores no ambiente escolhido
    data[ambiente].update(dados)

    # Reescreve o arquivo
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Limpa cache para refletir as mudanças
    global _config_cache
    _config_cache = None

    return True

# -----------
# import sqlite3
# from datetime import datetime
# from config import _RAIZ_PROJETO
# import os
# import json

# _config_cache = None


# def caminhos(ambiente_escolhido=None):
#     global _config_cache
#     if _config_cache is not None and ambiente_escolhido is None:
#         return _config_cache

#     ambiente = None  # 🔹 garante que a variável exista

#     # 🔹 1. Se não foi passado ambiente, tenta pegar do config.json
#     if ambiente_escolhido is None:
#         try:
#             camm = os.path.join(_RAIZ_PROJETO, "data", "config.json")
#             with open(camm, "r", encoding="utf-8") as f:
#                 ambiente = json.load(f).get("ambiente")
#         except Exception as e:
#             print("⚠️ Não foi possível ler config.json, usando fallback do banco:", e)  # noqa
#     else:
#         ambiente = ambiente_escolhido

#     # 🔹 fallback se ainda estiver vazio
#     if not ambiente:
#         ambiente = "Prod"

#     conn = sqlite3.connect("C:\\script\\titanic\\data\\banco.db")
#     cur = conn.cursor()
#     cur.execute(
#         "SELECT chave, valor FROM config_ambiente WHERE ambiente = ?",
#         (ambiente,))
#     rows = cur.fetchall()
#     conn.close()

#     cfg = {k: v for k, v in rows}

#     LOGS = os.path.join(_RAIZ_PROJETO, "logs")
#     NM_LOG = datetime.now().strftime('%Y-%m-%d') + '.log'
#     os.makedirs(LOGS, exist_ok=True)

#     _config_cache = {
#         "MINHA_RAIZ": _RAIZ_PROJETO,
#         "AMBIENTE": ambiente,
#         "LOGS": LOGS,
#         "NM_LOG": NM_LOG,
#         **cfg
#     }

#     return _config_cache


# # from utils.caminhos import _config_cache
# def salvar_caminho(ambiente, dados: dict):
#     caminho = caminhos()
#     DB_PATH = caminho['BANCOSQLITE']
#     """
#     Atualiza ou insere chaves/valores na tabela config_ambiente
#     para o ambiente especificado.
#     """
#     if not ambiente or not dados:
#         raise ValueError("Ambiente e dados devem ser fornecidos")

#     conn = sqlite3.connect(DB_PATH)
#     cur = conn.cursor()

#     try:
#         for chave, valor in dados.items():
#             cur.execute("""
#                 INSERT INTO config_ambiente (ambiente, chave, valor)
#                 VALUES (?, ?, ?)
#                 ON CONFLICT(ambiente, chave) DO UPDATE SET valor=excluded.valor  # noqa
#             """, (ambiente, chave, valor))
#         conn.commit()
#     except Exception as e:
#         conn.rollback()
#         raise e
#     finally:
#         conn.close()

#     # Limpa cache para refletir mudanças
#     global _config_cache
#     _config_cache = None

# -----------
# import sqlite3
# from datetime import datetime
# from config import _RAIZ_PROJETO
# import os

# _config_cache = None


# def caminhos(ambiente_escolhido=None):
#     global _config_cache
#     if _config_cache is not None and ambiente_escolhido is None:
#         return _config_cache

#     conn = sqlite3.connect("C:\\script\\titanic\\data\\banco.db")
#     cur = conn.cursor()

#     if ambiente_escolhido is None:
#         # pega o primeiro ambiente padrão
#         cur.execute("SELECT DISTINCT ambiente FROM config_ambiente LIMIT 1")
#         ambiente = cur.fetchone()[0]
#     else:
#         ambiente = ambiente_escolhido

#     cur.execute(
#         "SELECT chave, valor FROM config_ambiente WHERE ambiente = ?",
#         (ambiente,))
#     rows = cur.fetchall()
#     conn.close()

#     cfg = {k: v for k, v in rows}

#     LOGS = os.path.join(_RAIZ_PROJETO, "logs")
#     NM_LOG = datetime.now().strftime('%Y-%m-%d') + '.log'
#     os.makedirs(LOGS, exist_ok=True)

#     _config_cache = {
#         "MINHA_RAIZ": _RAIZ_PROJETO,
#         "AMBIENTE": ambiente,
#         "LOGS": LOGS,
#         "NM_LOG": NM_LOG,
#         **cfg
#     }

#     return _config_cache


# # from utils.caminhos import _config_cache
# def salvar_caminho(ambiente, dados: dict):
#     caminho = caminhos()
#     DB_PATH = caminho['BANCOSQLITE']
#     """
#     Atualiza ou insere chaves/valores na tabela config_ambiente
#     para o ambiente especificado.
#     """
#     if not ambiente or not dados:
#         raise ValueError("Ambiente e dados devem ser fornecidos")

#     conn = sqlite3.connect(DB_PATH)
#     cur = conn.cursor()

#     try:
#         for chave, valor in dados.items():
#             cur.execute("""
#                 INSERT INTO config_ambiente (ambiente, chave, valor)
#                 VALUES (?, ?, ?)
#                 ON CONFLICT(ambiente, chave) DO UPDATE SET valor=excluded.valor  # noqa
#             """, (ambiente, chave, valor))
#         conn.commit()
#     except Exception as e:
#         conn.rollback()
#         raise e
#     finally:
#         conn.close()

#     # Limpa cache para refletir mudanças
#     global _config_cache
#     _config_cache = None
