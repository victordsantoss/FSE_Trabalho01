from socket import *
import os

default_host = gethostname()
default_port = 55562 
default_message = ''

central_server_host = default_host
central_server_port = default_port
central_server = socket(AF_INET, SOCK_STREAM)

central_server.bind((central_server_host, central_server_port))
central_server.listen(5)
print(f'Servidor Central conectado no HOST:  {central_server_host} e PORTA: {central_server_port}')

distributed_server_connection, distributed_server_address = central_server.accept()
print(f'O Servidor distribuido: {distributed_server_address} se conectou')

while 1:
    print('=================================================')
    print('============= FSE - TRABALHO 01 =================')
    print('=================================================')
    new_message = input('1 - VER DISPOSITIVOS\n2 - ATUALIZAR ESTADOS\n')
    distributed_server_connection.send(new_message.encode());

    message_received = distributed_server_connection.recv(1024)
    print(message_received.decode())

    clear_page = int(input('LIMPAR TELA (1)\n'))
    if clear_page == 1:
        os.system('clear')


distributed_server_connection.close()