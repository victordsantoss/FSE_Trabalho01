from socket import *

default_host = gethostname()
default_port = 55552

distributed_server = socket(AF_INET, SOCK_STREAM)
distributed_server.connect((default_host, default_port))

while 1:
    message_send = input('Digite sua mensagem: ')
    distributed_server.send(message_send.encode())
