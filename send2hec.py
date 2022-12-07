import logging
import os
import sys
from typing import NewType

import paho.mqtt.client as mqtt
import requests
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, HTTPError
from requests.packages import urllib3

from classes import Broker, HecAPI, Metric
from log import set_log

urllib3.disable_warnings()

set_log()

load_dotenv()  # take environment variables from .env.
config_file = os.getenv("MQTT_CONFIG_FILE", "mqtt.conf")

broker = Broker()
broker.config(config_file)

hec_api = HecAPI()
hec_api.config(config_file)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.debug(f"Connected to MQTT With Result Code {rc}")
        client.subscribe(broker.topic, qos=1)
    else:
        logging.error(f"Connection to broker {broker.host} failed with {rc}")


def on_message(client, userdata, message):
    hec_post(topic=message.topic, payload=message.payload.decode())


Status = NewType("Status", bool)
Topic = NewType("Topic", str)
Payload = NewType("Payload", str)


def hec_post(topic: Topic, payload: Payload) -> Status:
    """Post received message to Splunk

    Transfer the payload received to Splunk using HTTP Event Collector

    Args:
        topic (str): The full MQTT topic path subscribed
        patload (str): The MQTT payload containing the measured value

    Returns:
       Status: bool the execution status of the POST
    """

    post_status = Status(False)
    metric = Metric(topic, payload)

    logging.info(f"Topic: {metric.topic}")
    logging.debug(f"Payload: {metric.payload}")
    logging.debug(f"SourceType: {metric.sourcetype}")

    try:
        r = requests.post(
            hec_api.url(),
            headers=hec_api.authHeader(),
            json=metric.post_data(),
            verify=False,
        )
        r.raise_for_status()
    except ConnectionError as _err:
        logging.error(f"Splunk refused connection: {_err}")
        return post_status
    except HTTPError as _err:
        logging.error(f"HTTP Error: {_err}")
        return post_status
    except Exception as _err:
        logging.error(_err)
        return post_status

    logging.debug("Successful connection to Splunk")
    # Check Splunk return code
    try:
        code = r.json()["code"]
        text = r.json()["text"]

    except Exception as _err:
        logging.error(f"No valid JSON returned from Splunk; {_err}")
        return post_status

    if code != 0:
        logging.error(f"Splunk error code: {code}")
        return post_status
    else:
        logging.info(f"Splunk HEC POST result: {text}")
        post_status = Status(True)

    return post_status


def main():

    client = mqtt.Client("Send2HEC")
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        logging.debug(f"Connecting to {broker.host}:{broker.port}")
        client.connect(broker.host, broker.port, 60)
        logging.info(f"Connected to {broker.host}:{broker.port}")

    except Exception as _err:
        logging.error(f"Connection to {broker.host}:{broker.port} failed: {_err}")
        sys.exit(1)

    client.loop_forever()


if __name__ == "__main__":
    main()
