from trn_domingo.trn_domingo import (gera_expurgo, executa,
                                     opc_dados, insert_sqlite, data_exec)
from datetime import datetime, timedelta, time
from utils.caminhos import caminhos
from utils.logs_escrita import log_info


def dia_da_semana():
    caminho = caminhos()
    data_banco = data_exec()
    # data_banco = datetime.strptime(data_banco, '%Y-%m-%d').date()
    nm_log_data = datetime.strftime(datetime.now(), '%d_%m_%Y')
    hoje = datetime.now()
    hoje_date = datetime.now().date()
    hora_atual_str = hoje.strftime("%H:%M:%S")
    hora_comp = datetime.now().time().replace(microsecond=0)
    dia = hoje.weekday()  # 0=segunda, 6=domingo
    ontem = hoje - timedelta(days=1)
    ontem = ontem.strftime('%d/%m/%Y')
    hora_limite_a = time(1, 20)
    hora_limite_b = time(20, 20)
    print(f'Hora atual: {hora_limite_a}, Dia da semana: {hora_limite_b}')

    if dia == int(caminho['RP_DIA_ABON']):  # Se for domingo
        if data_banco is None or datetime.strptime(data_banco, '%Y-%m-%d').date() < hoje_date:  # noqa  # Se não executou
            if hora_comp > hora_limite_a and hora_comp < hora_limite_b:
                log_info('A rotina de criação de expurgos iniciou')

                lista_trn = executa(
                    caminho['RP_EXP_DOMIN_BASE'], nm_log_data)
                lista_opc = opc_dados(
                    caminho['RP_OPC'],
                    caminho['RP_EXP_DOMIN_BASE'], nm_log_data)
                gera_expurgo(lista_trn, lista_opc, caminho['RP_EXP_DOMIN'], ontem)  # noqa

                insert_sqlite([('trn domingo', hoje_date,
                                hora_atual_str, 'automatica')])

                log_info('A rotina de criação de expurgos concluíu!')

            else:
                log_info('A rotina não executará hoje, programado para Segunda!')  # noqa

                return False

        else:
            log_info('A rotina não executará hoje, programado para Segunda!')

            return False
    else:
        log_info('A rotina não executará hoje, programado para Segunda!')

        return False
