# utils/database.py
import sqlite3
from utils.caminhos import caminhos


def carregar_caminhos_salvos():
    caminho = caminhos()
    DB_PATH = caminho['BANCOSQLITE']
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT ambiente FROM config_ambiente")
    ambientes = [row[0] for row in cur.fetchall()]
    conn.close()
    return ambientes
