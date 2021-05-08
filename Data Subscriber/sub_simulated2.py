import paho.mqtt.client as mqtt
import time
from datetime import datetime
import json
import psycopg2 as pg

conn = pg.connect("postgres://tebrulbkmheomn:7177e8431bf6054048be07c918399916c4952e2db2c8733894f9b8023680dcf6@ec2-54-164-238-108.compute-1.amazonaws.com:5432/dad2ns6usp82fa",sslmode="require")
#conn = pg.connect("postgres://xmtpoytqxrgjgu:f814f8c9fb2c598a1b7d93c0a09e4402ac07b3ccf4bb1a6f0762439b6f667a3e@ec2-34-230-167-186.compute-1.amazonaws.com:5432/df3eec6e7g1jr6", sslmode="require")

try:
    cur = conn.cursor()
    print("Connection Established")
except (Exception, pg.DatabaseError) as error:
    print(error)


def on_connect(client, userdata, flags, rc):
    print("Connected with Result Code: {}".format(rc))

def on_log(client, userdata, level, buffer):
    print("Log: ", buffer)

def on_message(client, userdata, message):
    print("Received message:", message.topic)
    msg = message.payload.decode("utf-8")
    dataObj=json.loads(msg)
    
    machine_id = 1004
    date = dataObj["date"]
    timestamp = dataObj["seconds"]
    temperature = dataObj["Temperature"]
    pressure = dataObj["Pressure"]
    humidity = dataObj["Humidity"]

    insertQ = """ INSERT INTO shohan."sensorData3" ("machine_id", "timestamp", "date", "pressure", "temperature", "humidity")
                    VALUES(%s,%s,%s,%s,%s,%s)"""
    record = (machine_id, timestamp, date, pressure, temperature, humidity)

    try:
        cur.execute(insertQ, record)
        print("DB Transaction executed")
        
        #commit all transactions after the loop has stopped.
        conn.commit()
        print("All DB Transactions committed")

    except (Exception, pg.DatabaseError) as error:
        print(error)



#MAIN
mqttBroker = "broker.hivemq.com"

client = mqtt.Client("Sensor 4")
client.connect(mqttBroker)

#call-back functions
client.on_connect = on_connect
client.on_log = on_log
client.on_message = on_message


client.loop_start()

client.subscribe("Shohan/M4/SenData")
time.sleep(1000)

client.loop_stop()