from socket import *
import RPi.GPIO as GPIO
import adafruit_dht
import time
import threading
import json

# JSON CONFIGS
with open("../utils/configuracao_sala_01.json", encoding='utf-8') as meu_json:
    devices = json.load(meu_json)

# SERVER CONFIGS
default_host = gethostname()
default_port = 55562
distributed_server = socket(AF_INET, SOCK_STREAM)
distributed_server.connect((default_host, default_port))

# GPIO CONFIGS
def handleGPIOConfig():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # DISPOSITIVOS DE SAÍDA
    GPIO.setup(devices["outputs"][0]["gpio"], GPIO.OUT) # "L_01": 18
    GPIO.setup(devices["outputs"][1]["gpio"], GPIO.OUT) # "L_02": 23
    GPIO.setup(devices["outputs"][2]["gpio"], GPIO.OUT) # "PR": 25
    GPIO.setup(devices["outputs"][3]["gpio"], GPIO.OUT) # "AC": 24
    GPIO.setup(devices["outputs"][4]["gpio"], GPIO.OUT) # "AL_BZ": 8
    # DISPOSITIVOS DE ENTRADA
    GPIO.setup(devices["inputs"][0]["gpio"], GPIO.OUT) # "SPres": 7
    GPIO.setup(devices["inputs"][1]["gpio"], GPIO.OUT) # "SFum": 1
    GPIO.setup(devices["inputs"][2]["gpio"], GPIO.OUT) # "SJan": 12
    GPIO.setup(devices["inputs"][3]["gpio"], GPIO.OUT) # "SPor": 16
    GPIO.setup(devices["inputs"][4]["gpio"], GPIO.OUT) # "SC_IN": 20
    GPIO.setup(devices["inputs"][5]["gpio"], GPIO.OUT) # "SC_OUT": 21

def handleOutputDevices():
    L_01 =  "ON" if GPIO.input(devices["outputs"][0]["gpio"]) == 1 else "OF"
    L_02 = "ON" if GPIO.input(devices["outputs"][1]["gpio"]) == 1 else "OF"
    PR = "ON" if GPIO.input(devices["outputs"][2]["gpio"]) == 1 else "OF"
    AC = "ON" if GPIO.input(devices["outputs"][3]["gpio"]) == 1 else "OF"
    AL_BZ = "ON" if GPIO.input(devices["outputs"][4]["gpio"]) == 1 else "OF"
    return '\nLEITURA DE DISPOSITIVOS DE SAÍDA: \n' + 'L01:'  + L_01 + '\n' + 'L_02: '  + L_02 +  '\n' + 'AC: '  + AC + '\n' + 'PR: ' + PR + '\n' + 'AL_BZ: ' + AL_BZ +'\n'

def handleInputDevices():
    SPres =  "ON" if GPIO.input(devices["inputs"][0]["gpio"]) == 1 else "OF"
    SFum = "ON" if GPIO.input(devices["inputs"][1]["gpio"]) == 1 else "OF"
    SJan = "ON" if GPIO.input(devices["inputs"][2]["gpio"]) == 1 else "OF"
    SPor = "ON" if GPIO.input(devices["inputs"][3]["gpio"]) == 1 else "OF"
    SC_IN = "ON" if GPIO.input(devices["inputs"][4]["gpio"]) == 1 else "OF"
    SC_OUT = "ON" if GPIO.input(devices["inputs"][5]["gpio"]) == 1 else "OF"
    return '\nLEITURA DE DISPOSITIVOS DE ENTRADA: \n' + 'SPres:'  + SPres + '\n' + 'SFum: '  + SFum +  '\n' + 'SJan: '  + SJan + '\n' + 'SPor: ' + SPor + '\n' + 'SC_IN: ' + SC_IN + '\n' + 'SC_OUT: ' + SC_OUT + '\n'

def handleTemperature():
    dhtDevice = adafruit_dht.DHT22(devices["sensor_temperatura"][0]["gpio"], GPIO.OUT) # "DHT22": 4
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
    return handleOutputDevices()
     
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