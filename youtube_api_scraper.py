from datetime import date, timedelta, datetime
from googleapiclient.discovery import build 
from gspread_dataframe import set_with_dataframe
from pytz import timezone
import pytz
import base64
import gspread
import pandas as pd

import json
import os

youTubeApiKey = os.environ["YOUTUBE_API_KEY"]
youtube = build('youtube', 'v3', developerKey=youTubeApiKey) #Parâmetros da API

channel_id = os.environ["MY_CHANNEL"]

uploads = youtube.channels().list(id=channel_id, part='contentDetails').execute() #Obtendo os dados da playlist 'uploads' do canal, que contém todos os seus vídeos

playlist_id = uploads['items'][0]['contentDetails']['relatedPlaylists']['uploads'] #Filtrando a consulta só com ID da playlist uploads

videos = [] #Criando uma lista vazia para armazenar os vídeos
next_page_token = None #Definindo a variável para o token da próxima página 
                        #a API do YT só permite 50 resultados por página

while True:   #loop para iterar por cada página da consulta na API e armazenar os vídeos na lista
    all_videos = youtube.playlistItems().list(playlistId=playlist_id, 
                                       part='snippet', 
                                       maxResults=50,
                                       pageToken=next_page_token).execute()
    
    videos += all_videos['items'] 
    next_page_token = all_videos.get('nextPageToken')
    
    if next_page_token is None: #Caso não haja o token, o loop é interrompido
        break
        
videos_ids = [video['snippet']['resourceId']['videoId'] for video in videos] #Filtrando os IDs de cada video
stats = [] #Criando uma lista vazia para armazenar as estatísticas de cada ID/vídeo

for video_id in videos_ids:
    res = youtube.videos().list(part='statistics', id=video_id).execute()
    stats += res['items']
    
channel_title = [video['snippet']['channelTitle'] for video in videos]  #Organizando as informações em listas
videos_title = [video['snippet']['title'] for video in videos]
url_thumbnails = [video['snippet']['thumbnails']['high']['url'] for video in videos]
published_date = [video['snippet']['publishedAt'] for video in videos]
video_description = [video['snippet']['description'] for video in videos]
videoid = [video['snippet']['resourceId']['videoId'] for video in videos]
extraction_date = [str(datetime.now(timezone('America/Sao_Paulo')))]*len(videos_ids)
video_link_string = 'https://www.youtube.com/watch?v='
video_link = [video_link_string + video for video in videoid]
liked = []
disliked = []
views = []
comment = []

for video in stats:
    liked.append(video['statistics'].get('likeCount')) 
    disliked.append(video['statistics'].get('dislikeCount'))
    views.append(video['statistics'].get('viewCount'))
    comment.append(video['statistics'].get('commentCount'))
        
df = pd.DataFrame({ #Transformando as listas em um dataframe
    'channel' :channel_title,
    'title':videos_title,
    'video_id':videoid,
    'link_video':video_link,
    'video_description':video_description,
    'published_date':published_date,
    'extraction_date':extraction_date,
    'likes':liked,
    'dislikes':disliked,
    'views':views,
    'comment':comment,
    'thumbnail': url_thumbnails})

decoded_content = os.environ["GOOGLE_SHEETS_CREDENTIALS"] #Credenciais do Google Sheets
decoded_credentials = base64.b64decode(decoded_content)
credentials = json.loads(decoded_credentials)

spreadsheet_id = os.environ["GOOGLE_SHEET_ID"]
service_account = gspread.service_account_from_dict(credentials)
sh = service_account.open_by_key(spreadsheet_id)

worksheet = sh.add_worksheet(title=f"{date.today()}", rows="1", cols="1") #Adicionando o dataframe em uma worksheet do Google Sheets
set_with_dataframe(worksheet, df)
