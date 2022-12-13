from socket import *
import RPi.GPIO as GPIO
import time

# SERVER CONFIGS 
default_host = gethostname()
default_port = 55562
distributed_server = socket(AF_INET, SOCK_STREAM)
distributed_server.connect((default_host, default_port))

# GPIO CONFIGS
def handleGPIOConfig():
    GPIO.setmode(GPIO.BCM)
    devices = {
        "L_01": 18, # LAMPADA 01 DA SALA ----- SAIDA
        "L_02": 23, # LAMPADA 02 DA SAL ----- SAIDA
        "AC": 24, # AR-CONDICIONADO ----- SAIDA
        "PR": 25, # PROJETO MULTIMÍDIA ----- SAIDA
        "AL_BZ": 8, # ALARME (BUZZER) ----- SAIDA
        "SPres": 7, # SENSOR DE PRESENÇA ----- ENTRADA
        "SFum": 1, # SENSOR DE FUMAÇA ----- ENTRADA
        "SJan": 12, # SENSOR DE JANELA T01 ----- ENTRADA
        "SPor": 16, # SENSOR DE JANELA T02 ----- ENTRADA
        "SC_IN": 20, # SENSOR DE CONTAGEM DE PESSOAS ENTRADA ----- ENTRADA
        "SC_OUT": 21, # SENSOR DE COTNAGEM DE PESSOAS SASIDA ----- ENTRADA
        "DHT22": 4, # SENSOR DE TEMPERATURA / UMIDADE HT22 ----- 1-WIRE
    }
    GPIO.setup(devices["L_01"], GPIO.OUT)
    GPIO.setup(devices["L_02"], GPIO.OUT)
    GPIO.setup(devices["AC"], GPIO.OUT)
    GPIO.setup(devices["PR"], GPIO.OUT)

def handleAllDevices():
    L_01 =  "LIGADO" if GPIO.input(18) == 1 else "DESLIGADO"
    L_02 = "LIGADO" if GPIO.input(23) == 1 else "DESLIGADO"
    AC = "LIGADO" if GPIO.input(24) == 1 else "DESLIGADO"
    PR = "LIGADO" if GPIO.input(25) == 1 else "DESLIGADO"
    return 'ESTADO L01:'  + L_01 + '\n' + 'ESTADO L_02: '  + L_02 +  '\n' + 'ESTADO AC: '  + AC + '\n' + 'ESTADO PR: ' + PR + '\n'


# ENVIO DE MENSAGENS 
def main():
    handleGPIOConfig()
    message_send = ''
    while 1:
        message_received = distributed_server.recv(1024)
        print(message_received.decode())

        if int(message_received.decode()) == 1: 
            message_send = handleAllDevices()
            distributed_server.send(message_send.encode())
        else:
            message_send = 'OUTRA'
            distributed_server.send(message_send.encode())

if __name__ == "__main__":
    main()