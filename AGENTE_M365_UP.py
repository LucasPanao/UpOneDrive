import os
import requests
import logging
import json
import msal
import yaml
import urllib3
from pathlib import Path
import shutil
from datetime import datetime
import configparser

configParser = configparser.RawConfigParser()   
configFilePath = "config.ini"
configParser.read(configFilePath)

### DECLARAÇÕES 
CLIENT_ID = configParser.get('my-config', 'CLIENT_ID')
TENANT_ID = configParser.get('my-config', 'TENANT_ID')
AUTHORITY_URL = configParser.get('my-config', 'AUTHORITY_URL')
RESOURCE_URL = configParser.get('my-config', 'RESOURCE_URL')
API_VERSION = configParser.get('my-config', 'API_VERSION')
USERNAME = configParser.get('my-config', 'USERNAME')
PASSWORD = configParser.get('my-config', 'PASSWORD')
SCOPES= configParser.get('my-config', 'SCOPES')
####


config = yaml.safe_load(open("parameters.json")) 

#Estabelece a conexão usando os dados do JSON

app = msal.ConfidentialClientApplication(
    config["client_id"], authority=config["authority"],
    client_credential=config["secret"],
    ) 

result = None 

# Primeiramente, procura um token do cache
# Como estamos procurando um token para o aplicativo atual, NÃO para um usuário final,
# observe que damos o parâmetro de conta como Nenhum.

result = app.acquire_token_silent(config["scope"], account=None)

if not result:
    logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
    result = app.acquire_token_for_client(scopes=config["scope"])

if "access_token" in result:
#Adquire o token e coloca os headers para a chamada da API
    app_to_onedrive = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY_URL)
    token = app_to_onedrive.acquire_token_by_username_password(USERNAME,PASSWORD,SCOPES)
    headers = {'Authorization': 'Bearer {}'.format(result['access_token'])}
    headers_2 = {'Authorization': 'Bearer {}'.format(result['access_token'])}

      

date = datetime.today().strftime('%Y-%m-%d')
files2 = open('list_folders.txt','r') #abre a lista de pastas
files = open('list_drive.txt','r') #abre a lista de drives dos usuarios
for line,line2 in zip(files.readlines(),files2.readlines()):
    id2 = line2.strip('\n')
    print(id2)
    onedrive_destination = line.strip('\n')
    print(onedrive_destination)
    if not os.path.exists(rf"C:\etc\%s\TO_UP\{date}"%id2):
        os.makedirs(rf"C:\etc\%s\TO_UP\{date}"%id2)   
    source = r"C:\etc\%s"%id2
    destination = rf"C:\etc\%s\TO_UP\{date}"%id2
    print(destination)
    for f in os.listdir(source):
    #Nesse caso está filtrando apenas determinados tipos de arquivos, mas pode-se escolher qualquer extensão. 
        if f.endswith(".mp4") or f.endswith(".txt") or f.endswith(".m4a") :
            shutil.move(source+'\\'+f, destination)
    local = destination

#Realiza um loop através dos arquivos dentro dos diretórios indicados
    for root, dirs, files in os.walk(local):
        for file_name in files:
            file_path = os.path.join(root,file_name)
            file_size = os.stat(file_path).st_size
            file_data = open(file_path, 'rb')
            print("O arquivo à ser enviado é: %s" %file_name)
            headers = headers_2
            if file_size < 4100000: 
                #Realiza um requisição simples quando o arquivo tem menos de 4mb 
                r = requests.put(onedrive_destination+"/"+file_name+":/content", data=file_data, headers=headers)
                print("O arquivo que foi enviado PELO PUT: %s" %file_name)
            else:
                #Cria uma sessão de Upload para arquivos maiores que 4mb
                print(onedrive_destination+"/"+file_name+":/createUploadSession",headers)
                upload_session = requests.post(onedrive_destination+"/"+file_name+":/createUploadSession", headers=headers).json()
                
                with open(file_path, 'rb') as f:
                    total_file_size = os.path.getsize(file_path)
                    chunk_size = 32768000
                    chunk_number = total_file_size//chunk_size
                    chunk_leftover = total_file_size - chunk_size * chunk_number
                    i = 0
                    while True:
                        chunk_data = f.read(chunk_size)
                        start_index = i*chunk_size
                        end_index = start_index + chunk_size
                        #Quando não existem mais dados a serem enviados do arquivo, realiza um break
                        if not chunk_data:
                            break
                        if i == chunk_number:
                            end_index = start_index + chunk_leftover
                        #Insere um header novo a cada upload de pacote
                        headers = {'Content-Length':'{}'.format(chunk_size),'Content-Range':'bytes {}-{}/{}'.format(start_index, end_index-1, total_file_size)}
                        #Realiza o upload de uma parte do arquivo por vez
                        chunk_data_upload = requests.put(upload_session['uploadUrl'], data=chunk_data, headers=headers)
                        print(chunk_data_upload)
                        print(chunk_data_upload.json())
                        i = i + 1
                    file_data.close()