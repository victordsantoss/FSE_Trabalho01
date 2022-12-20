import RPi.GPIO as GPIO

from tcpConfig import devices

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
    GPIO.setup(devices["inputs"][0]["gpio"], GPIO.IN) 
    GPIO.setup(devices["inputs"][1]["gpio"], GPIO.IN) 
    GPIO.setup(devices["inputs"][2]["gpio"], GPIO.IN)
    GPIO.setup(devices["inputs"][3]["gpio"], GPIO.IN) 
    GPIO.setup(devices["inputs"][4]["gpio"], GPIO.IN) 
    GPIO.setup(devices["inputs"][5]["gpio"], GPIO.IN) 