import os
import threading
import time

# EXTERNAL FILES 
from tcpConfig import handleTcpCentralConfig, devices
from csvConfig import handleCommandsSave, handleReadCsvCommands

distributed_server_connection, distributed_server_address = handleTcpCentralConfig()

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

def main():
    while 1:
        initialMenu('FSE - TRABALHO 01')
        commands = ''
        new_message = input('VER DISPOSITIVOS DE SAÍDA (1)\nVER DISPOSITIVOS DE ENTRADA (2)\nVER VALORES DE TEMPERATURA E UMIDADE (3)\nACIONAR/DESATIVAR DISPOSITIVOS DE SAÍDA INDIVIDUALMENTE(4)\nACIONAR/DESATIVAR TODOS DISPOSITIVOS DE SAÍDA(6)\nVISUALIZAR NÚMERO DE PESSOAS NA SALA (7)\nVISUALIZAR COMANDOS (9)\n')
        if int(new_message) >= 1 and int(new_message) < 4: commands = f'1,{new_message}'
        if int(new_message) == 4:
            os.system('clear')
            initialMenu('DISPOSITIVOS')
            for x in devices["outputs"]:
                print(f'Dispositivo: {x["tag"]} | ID de seleção: {x["gpio"]}')
            current_device = input('Selecione o dispositivo (DIGITE O ID DE SELEÇÃO): ')
            commands = f'2,{current_device}, outputs'

        if int(new_message) == 6:
            os.system('clear')
            initialMenu('DISPOSITIVOS')
            new_message = input('ACIONAR TODOS OS DISPOSITIVOS (1)\nDESATIVAR TODOS OS DISPOSITIVOS (2)\n')
            commands = f'3,{new_message}'

        if int(new_message) == 7: commands = f'1,{new_message}'
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