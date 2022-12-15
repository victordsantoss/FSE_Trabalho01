from socket import *
import os
import threading
import json

#scp -P 13508 -r centralServer.py victorlucas@164.41.98.16:./FSE_Trabalho01/src/services 

# JSON CONFIGS
with open("../utils/configuracao_sala_01.json", encoding='utf-8') as meu_json:
    dados = json.load(meu_json)

# default_host = dados['ip_servidor_central']
# default_port = dados['porta_servidor_central'] 
# default_message = ''

default_host = gethostname()
default_port = 55562 
default_message = ''

central_server_host = default_host
central_server_port = default_port
central_server = socket(AF_INET, SOCK_STREAM)

# scp -P 13508 -r centralServer.py victorlucas@164.41.98.16:

central_server.bind((central_server_host, central_server_port))
central_server.listen(5)
print(f'Servidor Central conectado no HOST:  {central_server_host} e PORTA: {central_server_port}')



distributed_server_connection, distributed_server_address = central_server.accept()
print(f'O Servidor distribuido: {distributed_server_address} se conectou')

def handleReceivedMessages(distributed_server_connection): 
    # Adicionar verificação se a mensagem é = ""
    # LEVAR THREAD para fora do while
    message_received = (distributed_server_connection.recv(1024)).decode()
    json_received = eval(message_received) 

    for device in json_received:
        print(f'Dispositivo: {device["tag"]}')
        print(f'Status: {device["state"]}\n')


def main():
    while 1:
        print('=================================================')
        print('============= FSE - TRABALHO 01 =================')
        print('=================================================')
        commands = ''
        new_message = input('VER DISPOSITIVOS DE ENTRADA (1)\nVER DISPOSITIVOS DE SAÍDA (2)\nVER VALORES DE TEMPERATURA E UMIDADE (3)\nACIONAR DISPOSITIVOS (4)\n')
        # OPCOES DE LEITURA
        if int(new_message) != 4:
            commands = f'1,{new_message}'
        # OPÇOES DE ESCRITA/MUDANÇA DE STADO
        if int(new_message) == 4:
            os.system('clear')
            print('=================================================')
            print('======== SELECIONE OS DISPOSITIVOS ==============')
            print('=================================================')
            new_message = input('L_01 (18)\nL_02 (23)\nAC (24)\nPR (25)\n')
            commands = f'2,{new_message}'

        distributed_server_connection.send(commands.encode())
        thread = threading.Thread(target=handleReceivedMessages, args=(distributed_server_connection,))
        thread.start()

        clear_page = int(input('LIMPAR TELA (1)\n'))
        if clear_page == 1:
            os.system('clear')


    distributed_server_connection.close()

if __name__ == "__main__":
    main()