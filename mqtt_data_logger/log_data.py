# ----------------------------------------------------------------------------
# Copyright (c) 2023, 4CSCC development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from mqtt_data_logger.sensor_data_models import (
    Topic,
    Sensor,
    Measurement,
    SensorMeasurement,
)


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

    # time = func.now(timezone=True)

    for measurement, value in measurements.items():
        if isinstance(value, list) | isinstance(value, tuple):
            str_value = value[0]
            value = value[1]
        else:
            str_value = ""

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
            measurement=[target_measurement],
            value=value,
            str_value=str_value,
        )
        session.add(measurement_record)

    session.commit()


def logged(session, number_of_records=25, sensor=None, measurement=None):
    """Get the latest sensor reading."""
    records = session.query(SensorMeasurement)
    if records is None:
        print("No records in the database.")
        return None
    elif sensor is not None:
        records = records.filter_by(sensor_id=sensor).one_or_none()
    elif measurement is not None:
        records = records.filter_by(measurement=measurement).one_or_none()
    else:
        records = records.order_by(SensorMeasurement.time.desc()) \
                  .head(number_of_records)
    for record in records:
        print(record)
    return records

# if __name__ == "__main__":
    # __spec__ = None
    # from mqtt_data_logger.util import start_session, test_path
    # session = start_session(test_path)
    # add_sensors_reading_record(session=session, measurements={"temp": 25.0, "humidity": 78.3})