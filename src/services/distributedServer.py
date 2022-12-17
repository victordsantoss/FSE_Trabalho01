 from socket import *

from markupsafe import string
import RPi.GPIO as GPIO
import adafruit_dht
import time
import threading
import json
import board

# JSON CONFIGS
with open("../utils/configuracao_sala_01.json", encoding='utf-8') as meu_json:
    devices = json.load(meu_json)

# SERVER CONFIGS
default_host = devices['ip_servidor_central']
default_port = devices['porta_servidor_central'] 
distributed_server = socket(AF_INET, SOCK_STREAM)
distributed_server.connect((default_host, default_port))

# GPIO CONFIGS
def handleGPIOConfig():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # DISPOSITIVOS DE SAÍDA
    GPIO.setup(devices["outputs"][0]["gpio"], GPIO.OUT)  
    GPIO.setup(devices["outputs"][1]["gpio"], GPIO.OUT)
    GPIO.setup(devices["outputs"][2]["gpio"], GPIO.OUT)  
    GPIO.setup(devices["outputs"][3]["gpio"], GPIO.OUT)  
    GPIO.setup(devices["outputs"][4]["gpio"], GPIO.OUT) 
    # DISPOSITIVOS DE ENTRADA
    GPIO.setup(devices["inputs"][0]["gpio"], GPIO.OUT) 
    GPIO.setup(devices["inputs"][1]["gpio"], GPIO.OUT) 
    GPIO.setup(devices["inputs"][2]["gpio"], GPIO.OUT)
    GPIO.setup(devices["inputs"][3]["gpio"], GPIO.OUT) 
    GPIO.setup(devices["inputs"][4]["gpio"], GPIO.OUT) 
    GPIO.setup(devices["inputs"][5]["gpio"], GPIO.OUT) 


def handleOutputDevices():
    res = [
        {
            "type": "lampada",
            "tag": "Lâmpada 01",
            "gpio": 18,
            "state": "ON" if GPIO.input(devices["outputs"][0]["gpio"]) == 1 else "OF"
        },
        {
            "type": "lampada",
            "tag": "Lâmpada 02",
            "gpio": 23,
            "state": "ON" if GPIO.input(devices["outputs"][1]["gpio"]) == 1 else "OF"

        },
        {
            "type": "projetor",
            "tag": "Projetor Multimidia",
            "gpio": 25,
            "state":  "ON" if GPIO.input(devices["outputs"][2]["gpio"]) == 1 else "OF"
        },
        {
            "type": "ar-condicionado",
            "tag": "Ar-Condicionado (1º Andar)",
            "gpio": 24,
            "state": "ON" if GPIO.input(devices["outputs"][3]["gpio"]) == 1 else "OF"
        },
        {
            "type": "alarme",
            "tag": "Sirene do Alarme",
            "gpio": 8,
            "state": "ON" if GPIO.input(devices["outputs"][4]["gpio"]) == 1 else "OF"
        }
    ]
    res = json.dumps(res)
    return res

def handleInputDevices():
    res = [
        {
          "type": "presenca",
          "tag": "Sensor de Presença",
          "gpio": 7,
          "state": "ON" if GPIO.input(devices["inputs"][0]["gpio"]) == 1 else "OF"
        },
        {
            "type": "fumaca",
            "tag": "Sensor de Fumaça",
            "gpio": 1,
            "state": "ON" if GPIO.input(devices["inputs"][1]["gpio"]) == 1 else "OF"
        },
        {
            "type": "janela",
            "tag": "Sensor de Janela",
            "gpio": 12,
            "state": "ON" if GPIO.input(devices["inputs"][2]["gpio"]) == 1 else "OF"
        },
        {
            "type": "porta",
            "tag": "Sensor de Porta",
            "gpio": 16,
            "state": "ON" if GPIO.input(devices["inputs"][3]["gpio"]) == 1 else "OF"
        },
        {
            "type": "contagem",
            "tag": "Sensor de Contagem de Pessoas Entrada",
            "gpio": 20,
            "state": "ON" if GPIO.input(devices["inputs"][4]["gpio"]) == 1 else "OF"
        },
        {
            "type": "contagem",
            "tag": "Sensor de Contagem de Pessoas Saída",
            "gpio": 21,
            "state": "ON" if GPIO.input(devices["inputs"][5]["gpio"]) == 1 else "OF"
        }
    ]
    res = json.dumps(res)
    return res

def handleTemperature():
    dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False) # "DHT22": 4
    try:
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temperature_f, temperature_c, humidity))
        if(temperature_c):
            return "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temperature_f, temperature_c, humidity)
        else:
            return 'ERRO NA LEITURA'
    except RuntimeError as error:
        return 'ERRO NA LEITURA'
    except Exception as error:
        return 'ERRO NA LEITURA'

def handleUpdateDeviceState(pin_number, device_type):
    GPIO.output(pin_number, GPIO.LOW) if GPIO.input(pin_number) == 1 else GPIO.output(pin_number, GPIO.HIGH)
    current_state = "ON" if GPIO.input(pin_number) == 1 else "OF"
    tag = ''
    device_type = device_type.strip()
    for d in devices[device_type]:
        if d["gpio"] == pin_number:
            tag = d["tag"]

    res = [
        {
            "tag": tag,
            "gpio": pin_number,
            "state": current_state
        }
    ]
    res = json.dumps(res)
    return res

def handleUpdateAllDevices(type):
    for x in devices['outputs']:
        print(f'Dispositivo: {x["tag"]} | ID de seleção: {x["gpio"]}')
        if GPIO.input(x["gpio"]) == 0 and type == 1:
            print(f'Dispositivo: {x["tag"]} | ESTÁ LIGADO')
            GPIO.output(x["gpio"], GPIO.HIGH) 
        if GPIO.input(x["gpio"]) == 1 and type == 2:
            print(f'Dispositivo: {x["tag"]} | ESTÁ LIGADO')
            GPIO.output(x["gpio"], GPIO.LOW) 
        print(GPIO.input(x["gpio"]))
        time.sleep(2.0)

    return handleOutputDevices()

def handleSendMessages(message_send):
    distributed_server.sendall(message_send.encode())

def main():
    handleGPIOConfig()
    while 1:
        message = distributed_server.recv(1024)
        print(message.decode())
        message = message.decode()
        message_received = message.split(',')

        if int(message_received[0]) == 1:  
            if int(message_received[1]) == 1:
                message_send = handleOutputDevices()
                threading.Thread(target=handleSendMessages, args=(message_send, )).start()
            elif int(message_received[1]) == 2:
                message_send = handleInputDevices()
                threading.Thread(target=handleSendMessages, args=(message_send, )).start()
            elif int(message_received[1]) == 3:
                    message_send = handleTemperature()
                    if message_send is not None:
                        distributed_server.sendall(message_send.encode())
                  
        if int(message_received[0]) == 2:
            message_send = handleUpdateDeviceState(int(message_received[1]), message_received[2])
            threading.Thread(target=handleSendMessages, args=(message_send, )).start()

        if int(message_received[0]) == 3:
            if int(message_received[1]) == 1:
                print('deve ativar todos os dispositivos')
                message_send = handleUpdateAllDevices(1)
                threading.Thread(target=handleSendMessages, args=(message_send, )).start()
            if int(message_received[1]) == 2:
                print('deve desativar todos os dispositivos')
                message_send = handleUpdateAllDevices(2)
                threading.Thread(target=handleSendMessages, args=(message_send, )).start()


# def handleAlarms():
#     GPIO.setup(devices["inputs"][1]["gpio"], GPIO.OUT) 
#     while 1:
#         state = "ON" if GPIO.input(devices["inputs"][1]["gpio"]) == 1 else "OF"
#         print("state", state, GPIO.input(devices["inputs"][1]["gpio"]))
#         if state == "ON":
#             print("TÁ ONLINE PORRA")
#             distributed_server.sendall(state.encode())
#         time.sleep(2.0)

# threading.Thread(target=handleAlarms).start()

if __name__ == "__main__":
    main()