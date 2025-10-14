from datetime import datetime
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from utils.caminhos import caminhos


caminho = caminhos()

# Variaveis
hora_atual = datetime.now()
nm_log_data = datetime.strftime(datetime.now(), '%Y-%m-%d')
CAMINHO_LOGS = caminho['MINHA_RAIZ']

nome_log = f'{nm_log_data}'

raiz_pasta = r'C:\\script\\titanic\\logs'

os.makedirs(raiz_pasta, exist_ok=True)
# TEMP
CAMINHO_LOGS = raiz_pasta

logger = logging.getLogger()
cwd = os.getcwd()
handler = TimedRotatingFileHandler(
    f'{CAMINHO_LOGS}\\{nm_log_data}.log',
    when='midnight', interval=1, backupCount=15)
handler.setFormatter(logging.Formatter(
    fmt='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S'))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def log_warning(message):
    if caminho['RP_ESC_LOG'] == 'Sim':
        logger.warning(message)


def log_info(message):
    if caminho['RP_ESC_LOG'] == 'Sim':
        logger.info(message)


def log_debug(message):
    if caminho['RP_ESC_LOG'] == 'Sim':
        logger.debug(message)


def log_critical(message):
    if caminho['RP_ESC_LOG'] == 'Sim':
        logger.info(message)


def log_error(message):
    if caminho['RP_ESC_LOG'] == 'Sim':
        logger.info(message)
