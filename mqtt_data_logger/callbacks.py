# ----------------------------------------------------------------------------
# Copyright (c) 2023, 4CSCC development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import json
import retry
from sqlite3 import OperationalError
from mqtt_data_logger.log_data import add_sensors_reading_record
from mqtt_data_logger.munge_wind import lookup_beaufort, lookup_cardinal


# Callbacks for Paho
def on_connect(client, userdata, flags, rc):
    """ "Generic on_connect function."""
    print("Connected with result code " + str(rc))
    client.subscribe("#")  # Subscribe to all topics


def on_message(client, userdata, msg):
    """Generic on_message function."""
    print(f"Topic: {msg.topic} Message: {str(msg.payload.decode())}")


def log_sensor_data(client, userdata, msg):
    """Provides callback for logging sensor_data."""
    global session
    if "session" not in globals():
        from mqtt_data_logger.util import start_session
        session = start_session()
    
    topic = msg.topic
    parsed_packet = json.loads(msg.payload.decode("utf-8"))
    measurements = parsed_packet["data"]
    if "wind_speed" in measurements:
        measurements["wind_speed_beaufort"] = lookup_beaufort(
            measurements["wind_speed"]
            )
        measurements.pop("wind_speed")

    if "wind_direction" in measurements:
        measurements["cardinal_direction"] = lookup_cardinal(
            measurements["wind_direction"]
            )

    sensor = parsed_packet["sensor"]
    print(f"Topic: {msg.topic} Message: {str(msg.payload.decode())}")
    try:
        add_sensors_reading_record(
            session=session,
            measurements=measurements,
            sensor=sensor,
            topic=topic
        )
    except OperationalError:
        retry.retry(
            add_sensors_reading_record,
            fargs=(session, measurements, sensor, topic),
            tries=3,
            delay=0.53,
        )
    except Exception as e:
        print(f"Error: {e}")
        raise e
    # add_sensors_reading_record(
        # session=session, measurements=measurements, sensor=sensor, topic=topic
    # )
