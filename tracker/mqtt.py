#!/usr/bin/env python3

import paho.mqtt.client as mqtt
from threading import Thread


class Mqtt(Thread):
    """
    Wrapper class for MQTT client
    """
    def __init__(self, ip, port, subscription, on_message, username, password):
        """
        Initialization
        :param ip: IP address of MQTT switch
        :param port: TCP port number
        :param subscription: Topic name
        :param on_message: Method name to process received messages
        """
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.subscription = subscription
        self.logger = open('mqtt.log', 'a+')
        self.mqttc = mqtt.Client()
        self.mqttc.on_connect = lambda mosg, obj, msg: self.mqttc.subscribe(self.subscription)
        self.mqttc.on_publish = lambda mosg, obj, mid: self.logger.write(str(mid) + '\n')
        self.mqttc.on_subscribe = lambda mosg, obk, mid, granted_qos: self.logger.write('Subscribed: ' + str(mid))
        self.mqttc.on_log = lambda mosg, obj, level, string: self.logger.write(string + '\n')
        self.mqttc.on_message = on_message
        self.start()

    def run(self):
        """
        Thread main loop
        :return:
        """
        try:
            self.mqttc.username_pw_set(username=self.username, password=self.password)
            self.mqttc.connect(self.ip, self.port, 60)
            self.mqttc.loop_forever()
        except ConnectionRefusedError as e:
            self.logger.write(e.strerror + '\n')
            print(e.strerror)

    def send(self, topic, message):
        """
        Send an MQTT message
        :param topic: Topic name to send on
        :param message: Messaage content to send
        :return:
        """
        self.mqttc.publish(topic, message)
