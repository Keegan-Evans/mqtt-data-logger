# ----------------------------------------------------------------------------
# Copyright (c) 2023, 4CSCC development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------


from pathlib import Path

from mqtt_data_logger.callbacks import on_connect, on_message, log_sensor_data
from paho.mqtt import client as mqtt

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


def start_session(db_fp=Path("/home/beta/sensor_data.db")):
    """Create a session to the database."""
    with db_fp as sqlite_filepath:
        engine = create_engine(f"sqlite:///{sqlite_filepath}")

        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()
        session.commit()
        return session


def get_mqtt_client():
    """Create a MQTT client."""
    client = client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.message_callback_add("sensor_data/#", log_sensor_data)

    try:
        client.connect("localhost", 1883, 60)
    except ConnectionRefusedError as ce:
        raise ce
    except Exception as e:
        raise e

    return client
