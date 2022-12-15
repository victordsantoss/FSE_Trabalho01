from socket import *
import os
import threading
import json
import csv
import datetime

count = 0
# JSON CONFIGS
with open("../utils/configuracao_sala_01.json", encoding='utf-8') as meu_json:
    dados = json.load(meu_json)

# default_host = dados['ip_servidor_central']
# default_port = dados['porta_servidor_central'] 

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

def handleReceivedMessages(distributed_server_connection): 
    message_received = (distributed_server_connection.recv(1024)).decode()
    json_received = eval(message_received) 
    for device in json_received:
        print(f'Dispositivo: {device["tag"]}')
        print(f'Status: {device["state"]}\n')

def handleCommandsSave(command):
    instruction = ''
    global count
    count += 1
    if (int(command[0]) == 1): instruction = 'VER DISPOSITIVOS DE ENTRADA'
    if (int(command[0]) == 2): instruction = 'VER DISPOSITIVOS DE SAÍDA'
    if (int(command[0]) == 3): instruction = 'VER VALORES DE TEMPERATURA E HUMIDADE'
    if (int(command[0]) == 4): instruction = 'ACIONAR DISPOSITIVOS'
    commands_data = [count, instruction, datetime.datetime.now()]
    with open('commands.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(commands_data)

def handleReadCsvCommands(): 
    with open('commands.csv', 'r') as file:
        csv_file = csv.reader(file, delimiter=",")
        for line in csv_file:
            print(line)

def main():
    while 1:
        print('=================================================')
        print('============= FSE - TRABALHO 01 =================')
        print('=================================================')
        commands = ''
        new_message = input('VER DISPOSITIVOS DE ENTRADA (1)\nVER DISPOSITIVOS DE SAÍDA (2)\nVER VALORES DE TEMPERATURA E UMIDADE (3)\nACIONAR DISPOSITIVOS (4)\nVISUALIZAR COMANDOS (5)\n')
        # OPCOES DE LEITURA
        if int(new_message) >= 1 and int(new_message) < 4:
            commands = f'1,{new_message}'
        # OPÇOES DE ESCRITA/MUDANÇA DE STADO
        if int(new_message) == 4:
            os.system('clear')
            print('=================================================')
            print('======== SELECIONE OS DISPOSITIVOS ==============')
            print('=================================================')
            new_message = input('L_01 (18)\nL_02 (23)\nAC (24)\nPR (25)\n')
            commands = f'2,{new_message}'

        primary_command = new_message.split(',')
        distributed_server_connection.send(commands.encode())
        handleCommandsSave(primary_command[0])
        thread = threading.Thread(target=handleReceivedMessages, args=(distributed_server_connection,))
        thread.start()

        if(int(primary_command[0]) == 5):
            handleReadCsvCommands()

        clear_page = int(input('LIMPAR TELA (1)\n'))
        if clear_page == 1:
            os.system('clear')

    distributed_server_connection.close()

if __name__ == "__main__":
    main()