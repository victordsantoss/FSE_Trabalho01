from socket import *

default_host = gethostname()
default_port = 55552
default_message = ''

central_server_host = default_host
central_server_port = default_port
central_server = socket(AF_INET, SOCK_STREAM)

central_server.bind((central_server_host, central_server_port))
central_server.listen(5)
print(f'Servidor Central conectado no HOST:  {central_server_host} e PORTA: {central_server_port}')

distributed_server_connection, distributed_server_address = central_server.accept()
print(f'O Servidor distribuido: {distributed_server_address} se conectou')

# Recebimento de mensagens
while 1:
    message_received = distributed_server_connection.recv(1024)
    if default_message != message_received:
        print(message_received.decode())

distributed_server_connection.close()