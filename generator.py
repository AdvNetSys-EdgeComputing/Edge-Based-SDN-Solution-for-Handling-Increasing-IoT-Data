#!/usr/bin/env python3

"""Data set for data generation is presented in a config.json file"""
"""Data is sent to MQTT broker via paho"""
"""Code a part of Advanced Network Systems project by Aditya Saroja Hariharakrishnan and Abhirami Shankar"""

import sys
import time
import random
import json

import paho.mqtt.client as mqtt

def generate (host, port, username, password, topic, sensors, intervalInMs, verbose):

    mqttClient = mqtt.Client ()

    if username:
        mqttClient.username_pw_set (username, password)

    mqttClient.connect (host, port)

    keys = list (sensors.keys ())
    intervalInS = intervalInMs / 200.0

    while True:
        sensorID = random.choice (keys)
        sensor = sensors [sensorID]
        minimumV, maximumV = sensor.get ("range", [0, 100])
        val = random.randint (minimumV, maximumV)

        data = {
            "id": sensorID,
            "value": val
        }

        for key in ["lat", "lng", "unit", "type", "description"]:
            value = sensor.get (key)

            if value is not None:
                data [key] = value

        payload = json.dumps (data)

        if verbose:
            print ("%s: %s" % (topic, payload))

        mqttClient.publish (topic, payload)
        time.sleep (intervalInS)


def main (jsonConfigPath):

    try:
        with open (jsonConfigPath) as handle:
            config = json.load (handle)
            jsonConfig = config.get ("mqtt", {})
            otherConfig = config.get ("misc", {})
            sensors = config.get ("sensors")

            intervalInMs = otherConfig.get ("intervalInMs", 500)
            verbose = otherConfig.get ("verbose", False)

            if not sensors:
                print ("no sensors specified in config, nothing to do")
                return

            host = jsonConfig.get ("host", "localhost")
            port = jsonConfig.get ("port", 1883)
            username = jsonConfig.get ("username")
            password = jsonConfig.get ("password")
            topic = jsonConfig.get ("topic", "mqttgen")

            generate (host, port, username, password, topic, sensors, intervalInMs, verbose)
    except IOError as error:
        print ("Error opening config file '%s'" % jsonConfigPath, error)

if __name__ == '__main__':
    if len (sys.argv) == 2:
        main (sys.argv [1])
    else:
        print ("usage %s config.json" % sys.argv [0])
