#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Speech.py: Speech a text from google tts."""

__author__  = "Kevin Daviet"
__version__ = "0.0.1"

import time, sys, os
import json
import paho.mqtt.client as mqtt

hostname = "192.168.1.16"
port     = 1883
clientId = "pc_desktop"
topic    = "maison/bureau"
# username = ""
# password= ""

# ============================================================================
# FUNCTIONS
# ============================================================================

# Callback when the client receives response from server
def on_connect(client, userdata, flags, rc):
	print("-------------------------------")
	print("Connexion topic "+topic+" "+str(rc))
	print("-------------------------------")
	client.subscribe(topic,1)

# Callback when a publish message is received from server.
def on_message(client, userdata, msg):
	print("Execute command : " + str(json.loads(msg.payload)['command']))
	try:
		#Exécution de la commande
		exec(json.loads(msg.payload)['command'])
	except Exception as e:
		print("Failed to execute command : " + str(json.loads(msg.payload)['command']))
	

# Fonction deconnexion broker
def on_disconnect(client, userdata, rc):
	print("on_disconnect")
	if rc != 0:
		print("Unexpected disconnection.")
	else:
		print("Deconnexion")

# ============================================================================
# /FUNCTIONS
# ============================================================================

# Config client
client = mqtt.Client(clientId, False, None, "MQTTv311", "tcp") #websockets
# Connexion /Reconnexion
client.on_connect = on_connect
# Réception message
client.on_message = on_message
# Déconnexion
client.on_disconnect = on_disconnect

try:
	# Connexion / écoute de message
	client.connect(hostname, port)
except Exception as e:
  print("Cannot connect to MQTT broker at %s:%d: %s" % (hostname, port, str(e)))
  raise

client.loop_forever()





