import logging
import os
import random
import time
import uuid

import paho.mqtt.client as mqtt
import schedule
from classes import Broker
from dotenv import load_dotenv

log_level = logging.DEBUG
log_format = "%(asctime)s %(levelname)s %(funcName)s %(message)s"
logging.basicConfig(level=log_level, format=log_format)

load_dotenv()  # take environment variables from .env.
config_file = os.getenv("CONFIG_FILE", "mqtt.conf")
broker = Broker()


board_id = f"{uuid.getnode():x}"  # get rid of leading 0x


def pub(client):
    _sensor_number = random.randint(0, 9)
    _sensor_path = f"Things/{board_id}/dht11-{_sensor_number}/air."
    _sensors = ["temperature", "humidity", "pressure"]

    for _sensor_name in _sensors:
        _measure = random.randint(0, 10000) / 100
        logging.debug(f"Publishing {_sensor_name}:{_measure}")
        client.publish(topic=f"{_sensor_path}{_sensor_name}", payload=_measure, qos=1, retain=False)


def conn(client):
    logging.debug(f"Connecting to {broker.host}:{broker.port}")
    try:
        client.connect(broker.host, broker.port, 60)
    except ConnectionError as _err:
        logging.error(f"Broker {broker.host}: {_err}")


def main():

    client = mqtt.Client()
    conn(client)
    schedule.every(60).seconds.do(conn, client)

    schedule.every(10).seconds.do(pub, client)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
