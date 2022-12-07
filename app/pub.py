import logging
import os
import random
import sys
import time
import uuid

import paho.mqtt.client as mqtt
import schedule
from classes import Broker
from dotenv import load_dotenv
from log import set_log

set_log()

load_dotenv()  # take environment variables from .env.
config_file = os.getenv("CONFIG_FILE", "mqtt.conf")

broker = Broker()
broker.config(config_file)
board_id = f"{uuid.getnode():x}"  # get rid of leading 0x
sensors = ["air.temperature", "air.humidity", "air.pressure"]


def pub(client):

    _sensor_number = random.randint(0, 9)
    _sensor_path = f"Things/{board_id}/dht11-{_sensor_number}/"
    _sensors = sensors

    logging.info(f"Publishing to {_sensor_path}")

    for _sensor_name in _sensors:
        _measure = random.randint(0, 10000) / 100
        logging.debug(f"Publishing {_sensor_name}:{_measure}")
        client.publish(topic=f"{_sensor_path}{_sensor_name}", payload=_measure, qos=1, retain=False)


def main():

    client = mqtt.Client("Pub")

    try:
        logging.debug(f"Connecting to {broker.host}:{broker.port}")
        client.connect(broker.host, broker.port, 60)
        logging.info(f"Connected to {broker.host}:{broker.port}")
    except Exception as _err:
        logging.error(f"Connection to {broker.host}:{broker.port} failed: {_err}")
        sys.exit(1)

    client.loop_start()  # MQTT keep alive

    schedule.every(10).seconds.do(pub, client)
    while True:
        schedule.run_pending()
        time.sleep(0.1)


if __name__ == "__main__":
    main()
