# SPDX-FileCopyrightText: 2023 Chris Murphy
# SPDX-License-Identifier: MIT
#
# A simple MQTT/Tk application to draw random rectangles when new Cheerlight colors
# are published.  Uses the MQTT broker run by Cheerlights.
#

#!/usr/bin/env python
#
# Import libraries
from tkinter import *
from random import random
import paho.mqtt.client as mqtt

# MQTT broker for Cheerlights
mqttHost = "mqtt.cheerlights.com"

# Create root windows and canvas
root = Tk()
root.geometry('800x800')
root.title('Cheerlights')
canvas = Canvas(root,bg='black',width=800,height=800)
canvas.pack()

# Define MQTT helper functions
def on_connect(mqttc, obj, flags, rc):
	print("Connected to %s:%s" % (mqttc._host, mqttc._port))
	mqttc.subscribe("hex", 0)
	
def on_disconnect(mqttc, obj, rc):
	print ('Disconnected, reconnecting...')
	mqttc.connect(mqttHost, 1883, 60)

def on_subscribe(mqttc, obj, mid, granted_qos):
	print("Subscribed: "+str(mid)+" "+str(granted_qos))

# This helper is the big one, drawing a random rectangle when a new color is published
def on_message(mqttc, obj, msg):
	global canvas
	print(msg.payload)
	x1 = int(random()*800)
	y1 = int(random()*800)
	x2 = int(random()*800)
	y2 = int(random()*800)
	canvas.create_rectangle(x1,y1,x2,y2,fill=msg.payload)
	
# Define the MQTT client instance
mqttc = mqtt.Client()

# Link the helper functions
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Connect to the MQTT broker
mqttc.connect(mqttHost, 1883, 60)

# Start MQTT and Tk loops
qttc.loop_start()
root.mainloop()





