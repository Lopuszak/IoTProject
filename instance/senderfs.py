#!/usr/bin/env python3
# TODO UNCOMMENT
import paho.mqtt.client as mqtt
import tkinter
from Handlers import *

# The terminal ID - can be any string.
terminal_id = "T0"
# The broker name or IP address.
# broker = "localhost"
broker = "localhost"
# broker = "127.0.0.1"
# broker = "10.0.0.1"

# The MQTT client.
client = mqtt.Client()



def call_worker(worker_name):
    client.publish("id/name", worker_name + "@" + terminal_id, )


def connect_to_broker():
    # Connect to the broker.
    client.connect(broker, keepalive=600)
    # Send message about conenction.
    print('connected!')
    call_worker("Client connected")


def disconnect_from_broker():
    # Send message about disconenction.
    call_worker("Client disconnected")
    # Disconnet the client.
    client.disconnect()
    print('disconnected!')


def run_sender():
    connect_to_broker()
    # create_main_window()

    # Start to display window (It will stay here until window is displayed)
    # window.mainloop()

    disconnect_from_broker()


def publish(card_id, timestamp):
    print('try to send:' + str(card_id) + '@' + str(timestamp))
    client.publish('id/card', str(card_id) + '@' + str(timestamp))


if __name__ == "__main__":
    # rfid = RFID()
    #TODO UNCOMMENT
    #rfid = MainController()


    # run_sender() this leave commeted
    connect_to_broker()

    while True:
        inp = ''
        # read = rfid.run()
        # if read is not None:
        #     print(f'{log_time} - read')
        #     publish(read, formated_print(log_time))
        while inp == "":
            inp = input()
        if inp.startswith('add '):
            print(f'adding new user')

        else:
            log_time = datetime.now()
            print(f'{log_time} - read')
            publish(inp, log_time)
        # time.sleep(0.1)

    disconnect_from_broker()
