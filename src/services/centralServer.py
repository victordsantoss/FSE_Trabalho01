from socket import *
import os

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

while 1:
    print('=================================================')
    print('============= FSE - TRABALHO 01 =================')
    print('=================================================')
    commands = ''
    new_message = input('VER DISPOSITIVOS DE ENTRADA (1)\nVER DISPOSITIVOS DE SAÍDA (2)\nVER VALORES DE TEMPERATURA E UMIDADE (3)\n ACIONAR DISPOSITIVOS (4)\n')
    commands = f'1,{new_message}'
    if int(new_message) != 4:
        distributed_server_connection.send(commands.encode());

    # if int(new_message) == 4:
    #     os.system('clear')
    #     print('=================================================')
    #     print('======== SELECIONE OS DISPOSITIVOS ==============')
    #     print('=================================================')
    #     new_message = input('L_01 (18)\nL_02 (23)\nAC (24)\n PR (25)\n')
    #     distributed_server_connection.send(new_message.encode());

    message_received = distributed_server_connection.recv(1024)
    print(message_received.decode())

    clear_page = int(input('LIMPAR TELA (1)\n'))
    if clear_page == 1:
        os.system('clear')


distributed_server_connection.close()
