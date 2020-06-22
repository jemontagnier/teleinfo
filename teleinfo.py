#!/usr/bin/python3
import time
import serial
import paho.mqtt.client as mqtt
ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=1200,                  # 1200 bauds
        bytesize = serial.SEVENBITS,    # 7bits
        parity = serial.PARITY_EVEN,    # parité paire
        stopbits = serial.STOPBITS_ONE, # un bit de stop
        xonxoff = False,                # pas de contrôle de flux
        timeout = 1
        )
def on_disconnect(mqtc, obj, rc):
    print("reconnecte")
    mqttc.reconnect()
print("Lancement téléinfo")
# creation du client MQTT
mqttc = mqtt.Client(client_id="teleinfo")
# set username/password
mqttc.username_pw_set("mqttusr", "mqttpasswd")
# connexion au relai
mqttc.connect("192.168.1.2", 1883, 60)
# pour traiter les éventuels évènements
mqttc.loop_start()
# boucle infinié
while 1:
    # lecture d'une ligne de données
    x = ser.readline()
    # on transforme en chaine et un peu de nettoyage
    x = x.decode('utf-8').rstrip()
    # on sépare les champs"
    c=x.split(' ')
    # puis on sélectionne ceux qui nous intesse
    #print (c)
    if c[0] == "BASE":
        mqttc.publish("teleinfo/base",int(c[1]))
    if c[0] == "IINST":
        mqttc.publish("teleinfo/iinst",int(c[1]))
        papp = int(c[1])*220
        mqttc.publish("teleinfo/papp",papp)
        #print (papp)
