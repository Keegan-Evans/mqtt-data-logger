# ----------------------------------------------------------------------------
# Copyright (c) 2023, 4CSCC development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from mqtt_data_logger.callbacks import on_connect, on_message, log_sensor_data

from pathlib import Path
import paho.mqtt.client as mqtt
import sys

Base = declarative_base()

with Path("/home/beta/sensor_data.db") as sqlite_filepath:
    engine = create_engine(f"sqlite:///{sqlite_filepath}")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
session.commit()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.message_callback_add("sensor_data/#", log_sensor_data)

# Connect to MQTT broker
try:
    client.connect("localhost", 1883, 60)
except ConnectionRefusedError:
    print("MQTT broker not running")
    sys.exit(1)

client.loop_forever()
