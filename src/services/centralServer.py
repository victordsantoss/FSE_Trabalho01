from socket import *
import os
import threading
import json
import csv
import datetime
import time

# JSON CONFIGS

sala = int(input("DESEJA CONECTAR EM QUAL SALA?\nSALA 01 (1)\nSALA 02 (2): "))
if sala == 1: 
    print('ENTREI SALA 01')
    with open("../utils/configuracao_sala_01.json", encoding='utf-8') as meu_json: devices = json.load(meu_json)
if sala == 2:
    print('ENTREI SALA 01')
    with open("../utils/configuracao_sala_02.json", encoding='utf-8') as meu_json: devices = json.load(meu_json)

default_host = devices['ip_servidor_central']
default_port = devices['porta_servidor_central'] 
default_message = ''

central_server_host = default_host
central_server_port = default_port
central_server = socket(AF_INET, SOCK_STREAM)

central_server.bind((central_server_host, central_server_port))
central_server.listen(5)
print(f'Servidor Central conectado no HOST:  {central_server_host} | PORTA: {central_server_port} | {devices["nome"]}')

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
    json_received = eval(message_received) 
    for device in json_received:
        print(f'Dispositivo: {device["tag"]}')
        print(f'Status: {device["state"]}')
        print(f'-----------------------------')

def handleGetCurrentDevice(type, pin_number):
    device = ""
    for d in devices[type.strip()]:
        if d["gpio"] == pin_number:
            device = d["tag"]
    return device

def handleCommandsSave(commands):
    instruction = ''
    commands = commands.split(',')
    if (int(commands[0]) == 1):
        if (int(commands[1]) == 1): instruction = 'VER DISPOSITIVOS DE SAÍDA'
        if (int(commands[1]) == 2): instruction = 'VER DISPOSITIVOS DE ENTRADA'
        if (int(commands[1]) == 3): instruction = 'VER VALORES DE TEMPERATURA E HUMIDADE'
        if (int(commands[1]) == 7): instruction = 'VER NÚMERO DE PESSOAS NA SALA'
    if (int(commands[0]) == 2):
        instruction = f'ACIONAMENTO/DESATIVAMENTO DO DISPOSITIVO {handleGetCurrentDevice(commands[2], int(commands[1]))}'
    if (int(commands[0]) == 3): 
        if (int(commands[1]) == 1): 
            instruction = 'ACIONAMENTO TODOS DISPOSITIVOS DE SAÍDA'
        if (int(commands[1]) == 2): 
            instruction = 'DESATIVAMENTO TODOS DISPOSITIVOS DE SAÍDA'

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
        new_message = input('VER DISPOSITIVOS DE SAÍDA (1)\nVER DISPOSITIVOS DE ENTRADA (2)\nVER VALORES DE TEMPERATURA E UMIDADE (3)\nACIONAR/DESATIVAR DISPOSITIVOS DE SAÍDA INDIVIDUALMENTE(4)\nACIONAR/DESATIVAR DISPOSITIVOS DE ENTRADA INDIVIDUALMENTE(5)\nACIONAR/DESATIVAR TODOS DISPOSITIVOS DE SAÍDA(6)\nVISUALIZAR NÚMERO DE PESSOAS NA SALA (7)\nVISUALIZAR COMANDOS (9)\n')
        if int(new_message) >= 1 and int(new_message) < 4: commands = f'1,{new_message}'
        if int(new_message) == 4 or int(new_message) == 5:
            os.system('clear')
            initialMenu('DISPOSITIVOS')
            device_type = "outputs" if int(new_message) == 4 else "inputs"
            for x in devices[device_type]:
                print(f'Dispositivo: {x["tag"]} | ID de seleção: {x["gpio"]}')
            current_device = input('Selecione o dispositivo (DIGITE O ID DE SELEÇÃO): ')
            commands = f'2,{current_device}, {device_type}'

        if int(new_message) == 6:
            os.system('clear')
            initialMenu('DISPOSITIVOS')
            new_message = input('ACIONAR TODOS OS DISPOSITIVOS (1)\nDESATIVAR TODOS OS DISPOSITIVOS (2)\n')
            commands = f'3,{new_message}'
            print('commands', commands)

        if int(new_message) == 7: commands = f'1,{new_message}'
        print(commands)
        if int(new_message) != 9: handleCommandsSave(commands)
        if int(new_message) == 9: handleReadCsvCommands()
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

        clear_page = int(input('LIMPAR TELA (8)\n'))
        if clear_page == 8: os.system('clear')

    distributed_server_connection.close()

if __name__ == "__main__":
    main()