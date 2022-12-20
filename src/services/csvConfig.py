import csv
import datetime
from tcpConfig import devices

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
    if (int(commands[0]) == 2): instruction = f'ACIONAMENTO/DESATIVAMENTO DO DISPOSITIVO {handleGetCurrentDevice(commands[2], int(commands[1]))}'
    if (int(commands[0]) == 3): 
        if (int(commands[1]) == 1): instruction = 'ACIONAMENTO TODOS DISPOSITIVOS DE SAÍDA'
        if (int(commands[1]) == 2): instruction = 'DESATIVAMENTO TODOS DISPOSITIVOS DE SAÍDA'
    commands_data = [instruction, datetime.datetime.now()]
    with open('commands.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(commands_data)

def handleReadCsvCommands(): 
    with open('commands.csv', 'r') as file:
        csv_file = csv.reader(file, delimiter=",")
        for line in csv_file:
            print(line)