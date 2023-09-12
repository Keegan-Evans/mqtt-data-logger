# ----------------------------------------------------------------------------
# Copyright (c) 2023, 4CSCC development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from sqlalchemy.sql import func
from mqtt_logger.sensor_data_models import (
    Topic,
    Sensor,
    Measurement,
    SensorMeasurement,
)

###############################################################################
# helper functions
###############################################################################


# DONE: add multiple sensor measurements at once
def add_sensors_reading_record(
    session,
    topic: str = "sensor_data",
    sensor: str = "env",
    measurements: dict = {"temp": 25.0, "humidity": 78.3},
):
    """Add a new measurement record to the database."""
    # create instance of SensorMeasurement
    target_topic = session.query(Topic).filter_by(topic=topic).one_or_none()
    if target_topic is None:
        target_topic = Topic(topic=topic)
        session.add(target_topic)

    sensor_id = session.query(Sensor).filter_by(sensor_id=sensor).one_or_none()
    if sensor_id is None:
        sensor_id = Sensor(sensor_id=sensor)
        session.add(sensor_id)

    time = func.now()

    for measurement, value in measurements.items():
        target_measurement = (
            session.query(Measurement)
            .filter_by(measurement=measurement)
            .one_or_none()
        )
        if target_measurement is None:
            target_measurement = Measurement(measurement=measurement)
            session.add(target_measurement)

        measurement_record = SensorMeasurement(
            topic=[target_topic],
            sensor=[sensor_id],
            time=time,
            measurement=[target_measurement],
            value=value,
        )
        session.add(measurement_record)

    session.commit()

    # TODO: refactor to own function
    for entry in session.query(SensorMeasurement):
        try:
            print(entry)
        except Exception:
            continue
