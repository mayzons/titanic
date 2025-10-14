# def adicona_data_expurgo(self):
#     mfunc = MinhasFuncs() # noqa
#     wb = load_workbook(TR_PASTA_DISP_EXPURGO, data_only=True)
#     ws = wb.active

#     # Encontrar a última linha com dados
#     ultima_linha = 0
#     for row in reversed(range(1, ws.max_row + 1)): # Percorre de trás para frente  #type: ignore # noqa
#         if any(cell.value is not None for cell in ws[row]):  # Verifica se há algum valor na linha #type: ignore # noqa
#             ultima_linha = row
#             break

#     # Verifica se encontrou uma linha com dados
#     if ultima_linha == 0:
#         print("Nenhuma data encontrada na planilha.")
#     else:
#         data_arq = ws[f"B{ultima_linha}"].value  # Obtém o valor da célula #type: ignore # noqa
#         usar_if_td_aqr = data_arq # noqa
#         if isinstance(data_arq, datetime):  # Se for um objeto datetime, tudo certo# noqa # noqa
#             data_formatada = data_arq.strftime('%d/%m/%Y')
#         else:
#             try:
#                 data_arq = datetime.strptime(str(data_arq), '%d/%m/%Y')
#                 data_formatada = data_arq.strftime('%d/%m/%Y')
#             except ValueError:
#                 print(f"Erro ao converter a data: {data_arq}")
#                 data_formatada = "Data inválida"

#         agora = datetime.now()
#         data_agora = (agora - timedelta(days=1)).strftime('%d/%m/%Y')
#         one_line = ultima_linha + 1
#         two_line = ultima_linha + 2

#         # Adiciona um dia à data do arquivo
#         data_insert = data_arq + timedelta(days=1)
#         data_formatada_insert = data_insert.strftime('%d/%m/%Y')

#     # Compara os dados da última linha com a data atual
#     if data_arq < agora: #type: ignore
#         ws[f'A{one_line}'] = 'ABASTECE V4 - Problema Geral - Conexão - SLT x Forseti TESTE'  #type: ignore # noqa
#         ws[f'B{one_line}'] = data_formatada_insert  #type: ignore
#         ws[f'C{one_line}'] = 'Sim'  #type: ignore
#         ws[f'A{two_line}'] = 'ABASTECE V4 - Problema Geral - Camera OCR'  #type: ignore # noqa
#         ws[f'B{two_line}'] = data_formatada_insert #type: ignore
#         ws[f'C{two_line}'] = 'Sim' #type: ignore

#         if LOG_ESCRITA.lower() == 'sim':
#             msg_log = f'Adiocionado a data {data_formatada_insert} no arquivo Expurgo Componente.xlsx'  #type: ignore # noqa
#             log_info(msg_log)

#     else:
#         if LOG_ESCRITA.lower() == 'sim':
#             msg_log = f'Data Expurgo {data_formatada_insert} já está em Expurgo Componente.xlsx'  #type: ignore # noqa
#             log_info(msg_log)

#     # Salva o arquivo atualizado
#     wb.save(TR_PASTA_DISP_EXPURGO)
#     wb.close()
