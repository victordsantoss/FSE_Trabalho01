from socket import *
import RPi.GPIO as GPIO
import time

# SERVER CONFIGS 
default_host = gethostname()
default_port = 55552
distributed_server = socket(AF_INET, SOCK_STREAM)
distributed_server.connect((default_host, default_port))


# GPIO CONFIGS
GPIO.setmode(GPIO.BCM)
dispositivos = {
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

GPIO.setup(dispositivos["L_01"], GPIO.OUT)
GPIO.setup(dispositivos["L_02"], GPIO.OUT)
GPIO.setup(dispositivos["AC"], GPIO.OUT)
GPIO.setup(dispositivos["PR"], GPIO.OUT)

while 1:
    lampada_1 =  "ligado" if GPIO.input(18) == 1 else "desligado"
    lampada_2 = "ligado" if GPIO.input(23) == 1 else "desligado"
    ar_condicionado = "ligado" if GPIO.input(24) == 1 else "desligado"
    projetor = "ligado" if GPIO.input(25) == 1 else "desligado"

    message_send =   'lampada 1 esta' + lampada_1 + '|' + 'lampada 2' + lampada_2 +  '|' + 'ar condicionado'  + ar_condicionado+ '|' + 'projetor esta' +projetor+ '.'

    distributed_server.send(message_send.encode())
    time.sleep(5)