from socket import *
import RPi.GPIO as GPIO
import adafruit_dht
import time
import threading

# SERVER CONFIGS
default_host = gethostname()
default_port = 55562
distributed_server = socket(AF_INET, SOCK_STREAM)
distributed_server.connect((default_host, default_port))

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
    "SC_OUT": 21, # SENSOR DE CONTAGEM DE PESSOAS SAÍDA ----- ENTRADA
    "DHT22": 4, # SENSOR DE TEMPERATURA / UMIDADE HT22 ----- 1-WIRE
}

# GPIO CONFIGS
def handleGPIOConfig():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # DISPOSITIVOS DE SAÍDA
    GPIO.setup(devices["L_01"], GPIO.OUT)
    GPIO.setup(devices["L_02"], GPIO.OUT)
    GPIO.setup(devices["AC"], GPIO.OUT)
    GPIO.setup(devices["PR"], GPIO.OUT)
    GPIO.setup(devices["AL_BZ"], GPIO.OUT)
    # DISPOSITIVOS DE ENTRADA
    GPIO.setup(devices["SPres"], GPIO.IN)
    GPIO.setup(devices["SFum"], GPIO.IN)
    GPIO.setup(devices["SJan"], GPIO.IN)
    GPIO.setup(devices["SPor"], GPIO.IN)
    GPIO.setup(devices["SC_IN"], GPIO.IN)
    GPIO.setup(devices["SC_OUT"], GPIO.IN)

def handleOutputDevices():
    L_01 =  "ON" if GPIO.input(devices["L_01"]) == 1 else "OF"
    L_02 = "ON" if GPIO.input(devices["L_02"]) == 1 else "OF"
    AC = "ON" if GPIO.input(devices["AC"]) == 1 else "OF"
    PR = "ON" if GPIO.input(devices["PR"]) == 1 else "OF"
    AL_BZ = "ON" if GPIO.input(devices["AL_BZ"]) == 1 else "OF"
    return '\nLEITURA DE DISPOSITIVOS DE SAÍDA: \n' + 'L01:'  + L_01 + '\n' + 'L_02: '  + L_02 +  '\n' + 'AC: '  + AC + '\n' + 'PR: ' + PR + '\n' + 'AL_BZ: ' + AL_BZ +'\n'

def handleInputDevices():
    SPres =  "ON" if GPIO.input(devices["SPres"]) == 1 else "OF"
    SFum = "ON" if GPIO.input(devices["SFum"]) == 1 else "OF"
    SJan = "ON" if GPIO.input(devices["SJan"]) == 1 else "OF"
    SPor = "ON" if GPIO.input(devices["SPor"]) == 1 else "OF"
    SC_IN = "ON" if GPIO.input(devices["SC_IN"]) == 1 else "OF"
    SC_OUT = "ON" if GPIO.input(devices["SC_OUT"]) == 1 else "OF"
    return '\nLEITURA DE DISPOSITIVOS DE ENTRADA: \n' + 'SPres:'  + SPres + '\n' + 'SFum: '  + SFum +  '\n' + 'SJan: '  + SJan + '\n' + 'SPor: ' + SPor + '\n' + 'SC_IN: ' + SC_IN + '\n' + 'SC_OUT: ' + SC_OUT + '\n'

def handleTemperature():
    dhtDevice = adafruit_dht.DHT22(devices["DHT22"])
    while True:
        try:
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity
            print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temperature_f, temperature_c, humidity))
            return "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temperature_f, temperature_c, humidity)
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error
        time.sleep(2.0)

def handleUpdateDeviceState(pin_number):
    print(pin_number, type(pin_number))
    GPIO.output(pin_number, GPIO.LOW) if GPIO.input(pin_number) == 1 else GPIO.output(pin_number, GPIO.HIGH)
    res = handleOutputDevices()
    return res
   
def handleSendMessages(message_send):
    distributed_server.send(message_send.encode())

def main():
    handleGPIOConfig()
    message_send = ''
    while 1:
        message = distributed_server.recv(1024)
        print(message.decode())
        message = message.decode()
        message_received = message.split(',')

        if int(message_received[0]) == 1:  
            if int(message_received[1]) == 1:
                message_send = handleOutputDevices()
            elif int(message_received[1]) == 2:
                message_send = handleInputDevices()
            elif int(message_received[1]) == 3:
                message_send = handleTemperature()
        if int(message_received[0]) == 2:
            message_send = handleUpdateDeviceState(int(message_received[1]))
            distributed_server.send(message_send.encode())
        send_thread = threading.Thread(target=handleSendMessages, args=(message_send, ))
        send_thread.start()

if __name__ == "__main__":
    main()