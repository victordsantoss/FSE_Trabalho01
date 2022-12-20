from socket import *
import json

# JSON CONFIGS
sala = int(input("DESEJA CONECTAR EM QUAL SALA?\nSALA 01 (1)\nSALA 02 (2): "))
if sala == 1: 
    with open("../utils/configuracao_sala_01.json", encoding='utf-8') as meu_json: devices = json.load(meu_json)
if sala == 2:
    with open("../utils/configuracao_sala_02.json", encoding='utf-8') as meu_json: devices = json.load(meu_json)

default_host = devices['ip_servidor_central']
default_port = devices['porta_servidor_central'] 
central_server = socket(AF_INET, SOCK_STREAM)

def handleTcpCentralConfig():
    central_server.bind((default_host, default_port))
    central_server.listen(5)
    print(f'Servidor Central conectado no HOST:  {default_host} | PORTA: {default_port} | {devices["nome"]}')

    distributed_server_connection, distributed_server_address = central_server.accept()
    print(f'O Servidor distribuido: {distributed_server_address} se conectou')
    return distributed_server_connection, distributed_server_address

def handleTcpDistriConfig():
    distributed_server = socket(AF_INET, SOCK_STREAM)
    distributed_server.connect((default_host, default_port))

    return distributed_server, sala