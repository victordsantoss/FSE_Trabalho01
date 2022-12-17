from socket import *
import os
import threading
import json
import csv
import datetime
import time

# JSON CONFIGS
with open("../utils/configuracao_sala_01.json", encoding='utf-8') as meu_json:
    devices = json.load(meu_json)

default_host = devices['ip_servidor_central']
default_port = devices['porta_servidor_central'] 
default_message = ''

central_server_host = default_host
central_server_port = default_port
central_server = socket(AF_INET, SOCK_STREAM)

central_server.bind((central_server_host, central_server_port))
central_server.listen(5)
print(f'Servidor Central conectado no HOST:  {central_server_host} e PORTA: {central_server_port}')

distributed_server_connection, distributed_server_address = central_server.accept()
print(f'O Servidor distribuido: {distributed_server_address} se conectou')

def initialMenu(string):
    print('=================================================')
    print(f'============= {string} =================')
    print('=================================================')

def handleReceivedTemperature(distributed_server_connection):
    try:
        message_received = (distributed_server_connection.recv(1024)).decode()
        print(message_received)
    except:
        print("ERRO NA LEITURA")

def handleReceivedMessages(distributed_server_connection): 
    message_received = (distributed_server_connection.recv(1024)).decode()
    if message_received != "":
        json_received = eval(message_received) 
        for device in json_received:
            print(f'Dispositivo: {device["tag"]}')
            print(f'Status: {device["state"]}')
            print(f'-----------------------------')
        
def handleCommandsSave(command):
    instruction = ''
    if (int(command[0]) == 1): instruction = 'VER DISPOSITIVOS DE ENTRADA'
    if (int(command[0]) == 2): instruction = 'VER DISPOSITIVOS DE SAÍDA'
    if (int(command[0]) == 3): instruction = 'VER VALORES DE TEMPERATURA E HUMIDADE'
    if (int(command[0]) == 4): instruction = 'ACIONAR DISPOSITIVOS'
    commands_data = [instruction, datetime.datetime.now()]
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
        initialMenu('FSE - TRABALHO 01')
        commands = ''
        new_message = input('VER DISPOSITIVOS DE ENTRADA (1)\nVER DISPOSITIVOS DE SAÍDA (2)\nVER VALORES DE TEMPERATURA E UMIDADE (3)\nACIONAR/DESATIVAR DISPOSITIVOS DE ENTRADA INDIVIDUALMENTE(4)\nACIONAR/DESATIVAR DISPOSITIVOS DE SAÍDA INDIVIDUALMENTE(5)\nACIONAR/DESATIVAR TODOS DISPOSITIVOS DE SAÍDA(6)\nVISUALIZAR COMANDOS (7)\n')
        # OPCOES DE LEITURA
        if int(new_message) >= 1 and int(new_message) < 4:
            commands = f'1,{new_message}'
        # OPÇOES DE ESCRITA/MUDANÇA DE STADO
        if int(new_message) == 4 or int(new_message) == 5:
            os.system('clear')
            initialMenu('DISPOSITIVOS')
            device_type = "outputs" if int(new_message) == 4 else "inputs"
            for x in devices[device_type]:
                print(f'Dispositivo: {x["tag"]} | ID de seleção: {x["gpio"]}')
            new_message = input('Selecione o dispositivo (DIGITE O ID DE SELEÇÃO): ')
            commands = f'2,{new_message}, {device_type}'

        if int(new_message) == 6:
            os.system('clear')
            initialMenu('DISPOSITIVOS')
            new_message = input('ACIONAR TODOS OS DISPOSITIVOS (1)\nDESATIVAR TODOS OS DISPOSITIVOS (2)\n')
            commands = f'3,{new_message}'
            print('commands', commands)


        primary_command = new_message.split(',')
        handleCommandsSave(primary_command[0])
        if int(new_message) == 3:
            while 1:
                try:
                    distributed_server_connection.send(commands.encode())
                    threading.Thread(target=handleReceivedTemperature, args=(distributed_server_connection,)).start()
                    time.sleep(2.0)
                except KeyboardInterrupt:
                    break
        else:
            distributed_server_connection.send(commands.encode())
            threading.Thread(target=handleReceivedMessages, args=(distributed_server_connection,)).start()
        
        if int(primary_command[0]) == 7:
            handleReadCsvCommands()

        clear_page = int(input('LIMPAR TELA (8)\n'))
        if clear_page == 8:
            os.system('clear')
    
    distributed_server_connection.close()

if __name__ == "__main__":
    main()