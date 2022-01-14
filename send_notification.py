from datetime import date, timedelta, datetime
from gspread_dataframe import set_with_dataframe
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import base64
import gspread
import pandas as pd


import json
import os

decoded_content = os.environ["GOOGLE_SHEETS_CREDENTIALS"] #Credenciais do Google Sheets
decoded_credentials = base64.b64decode(decoded_content)
credentials = json.loads(decoded_credentials)

spreadsheet_id = os.environ["GOOGLE_SHEET_ID"] #Colocando o ID da planilha
service_account = gspread.service_account_from_dict(credentials)
sh = service_account.open_by_key(spreadsheet_id)

worksheet_today = sh.worksheet(title=f"{date.today()}") #Identificando a worksheet do dia
worksheet_yesterday = sh.worksheet(title=f"{date.today() - timedelta(days=1)}") #Identificando a worksheet do dia anterior

today_list = worksheet_today.col_values(3) #Obtendo de todas as linhas da planilha da célula 3 (neste caso, são os IDs do vídeo)
yesterday_list = worksheet_yesterday.col_values(3)

today_set = set(today_list) #Transformando a lista em set
yesterday_set = set(yesterday_list)

excluded_ids = yesterday_set - today_set #Comparando os dados de ontem com os de hoje
excluded_videos = [video for video in worksheet_yesterday.get_all_records() if video['video_id'] in excluded_ids] #Caso haja alguma remoção, puxa todas as informações da planilha para o vídeo removido

excluded_df = pd.DataFrame(data=excluded_videos) #Transformando em um dataframe

send_grid_api_key = os.environ["SENDGRID_API_KEY"] #Autenticação do SendGrid
email_message = '''<p>Olá! Parece que um vídeo foi removido do YouTube.</p>
<p>Confira na tabela abaixo algumas informações.</p>''' #Criando mensagem do e-mail
email_message_bot = '''<p><em>Essa mensagem foi enviada por um robô. Dúvidas, sugestões ou bugs, encaminhe para alessandrofajunior@gmail.com</em></p>'''
    
    
if excluded_videos: #caso a lista contiver algum item, disparar e-mail
    email_table = excluded_df.to_html()
    email = Mail(
    from_email=os.environ["MY_EMAIL"],
    to_emails=os.environ["MY_EMAIL"],
    subject="Parece que um vídeo foi removido do YouTube!",
    html_content=f"{email_message} <br /> {email_table} <br /> {email_message_bot}",)
    client = SendGridAPIClient(send_grid_api_key)
    response = client.send(email)
