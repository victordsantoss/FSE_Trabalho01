from socket import *
import RPi.GPIO as GPIO
import adafruit_dht
import time
import threading
import json
import board

# EXTERNAL FILES 
from tcpConfig import devices, handleTcpDistriConfig
from gpioConfig import handleGPIOConfig

# SERVER CONFIGS
distributed_server, sala = handleTcpDistriConfig()

def handleOutputDevices():
    if (GPIO.input(devices["inputs"][0]["gpio"]) == 1) or (GPIO.input(devices["inputs"][2]["gpio"]) == 1):  GPIO.output(devices["outputs"][4]["gpio"], GPIO.HIGH) 
    else: GPIO.output(devices["outputs"][4]["gpio"], GPIO.LOW) 
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
            "state": "ALERTA ALARME ESTÁ ACIONADO!!" if GPIO.input(devices["outputs"][4]["gpio"]) == 1 else "OF"
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
    dhtDevice = adafruit_dht.DHT22(board.D18 if sala == 2 else board.D4, use_pulseio=False) 
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
        if GPIO.input(x["gpio"]) == 0 and type == 1:
            GPIO.output(x["gpio"], GPIO.HIGH) 
        if GPIO.input(x["gpio"]) == 1 and type == 2:
            GPIO.output(x["gpio"], GPIO.LOW) 
        print(f'Dispositivo: {x["tag"]} | ID de seleção: {x["gpio"]} | Estado: {"ON" if GPIO.input(x["gpio"]) == 1 else "OF"}')
        time.sleep(0.5)
    return handleOutputDevices()

def handleAlarms():
    GPIO.setup(devices["inputs"][0]["gpio"], GPIO.IN) 
    GPIO.setup(devices["inputs"][2]["gpio"], GPIO.IN) 
    GPIO.setup(devices["inputs"][3]["gpio"], GPIO.IN) 
    GPIO.setup(devices["outputs"][4]["gpio"], GPIO.OUT) 
    res = [
        {
          "type": "presenca",
          "tag": "Sensor de Presença",
          "gpio": 7,
          "state": "ON" if GPIO.input(devices["inputs"][0]["gpio"]) == 1 else "OF"
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

    ]
    while 1:
        for d in res:
            print (f'{d["tag"]}: {d["state"]}')
            if d["state"] == "ON":
                print(f'ALERTA! O SENSOR {d["tag"]} está LIGADO - O ALARME SERÁ ATIVADO')
                GPIO.output(devices["outputs"][4]["gpio"], GPIO.HIGH) 
        time.sleep(5.0)

aux = 0

def handleCountPeople():
    GPIO.setup(devices["inputs"][4]["gpio"], GPIO.IN) 
    GPIO.setup(devices["inputs"][5]["gpio"], GPIO.IN) 
    GPIO.add_event_detect(devices['inputs'][4]['gpio'], GPIO.RISING)
    GPIO.add_event_detect(devices['inputs'][5]['gpio'], GPIO.RISING)
    people = 0
    try:
        while 1:
            time.sleep(0.0001)
            if GPIO.event_detected(devices["inputs"][4]["gpio"]):
                people = people + 1
            if GPIO.event_detected(devices["inputs"][5]["gpio"]):
                people = people - 1
                if people < 0: people = 0
            aux = people
    except RuntimeError as error:
        print("error", error)

def main():
    handleGPIOConfig()
    while 1:
        message = distributed_server.recv(1024)
        message = message.decode()
        message_received = message.split(',')
        if int(message_received[0]) == 1:  
            if int(message_received[1]) == 1:
                message_send = handleOutputDevices()
                distributed_server.send(message_send.encode())
            elif int(message_received[1]) == 2:
                message_send = handleInputDevices()
                distributed_server.send(message_send.encode())
            elif int(message_received[1]) == 3:
                    message_send = handleTemperature()
                    if message_send is not None:
                        distributed_server.sendall(message_send.encode())
            elif int(message_received[1]) == 7:
                res = [
                    {
                        "tag": 'Sensor de Contagem de Pessoas',
                        "state": f'Número de Pessoas na sala: {aux}'
                    }
                ]
                res = json.dumps(res)
                distributed_server.send(res.encode())  

        if int(message_received[0]) == 2:
            message_send = handleUpdateDeviceState(int(message_received[1]), message_received[2])
            distributed_server.send(message_send.encode())

        if int(message_received[0]) == 3:
            if int(message_received[1]) == 1:
                message_send = handleUpdateAllDevices(1)
                distributed_server.send(message_send.encode())
            if int(message_received[1]) == 2:
                message_send = handleUpdateAllDevices(2)
                distributed_server.send(message_send.encode())

threading.Thread(target=handleAlarms,).start()
threading.Thread(target=handleCountPeople,).start()

if __name__ == "__main__":
    main()