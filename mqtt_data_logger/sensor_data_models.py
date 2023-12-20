# ----------------------------------------------------------------------------
# Copyright (c) 2023, 4CSCC development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------


from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    Float,
    TIMESTAMP,
    DateTime,
    create_engine,
)

from sqlalchemy.orm import (
    relationship,
    backref,
    sessionmaker,
    declarative_base,
)

from pathlib import Path

from sys import argv
from icecream import ic


Base = declarative_base()


###############################################################################
# connection tables
###############################################################################

topic_sensor_measurement = Table(
    "topic_sensor_measurement",
    Base.metadata,
    Column("topic_num_id", Integer, ForeignKey("topics.topic_num_id")),
    Column(
        "sensor_measurement_num_id",
        Integer,
        ForeignKey("sensor_measurements.sensor_measurement_num_id"),
    ),
)

sensor_sensor_measurement = Table(
    "sensor_sensor_measurement",
    Base.metadata,
    Column("sensor_num_id", Integer, ForeignKey("sensors.sensor_num_id")),
    Column(
        "sensor_measurement_num_id",
        Integer,
        ForeignKey("sensor_measurements.sensor_measurement_num_id"),
    ),
)

measurement_kind_sensor_measurement = Table(
    "measurement_kind_sensor_measurement",
    Base.metadata,
    Column(
        "measurement_num_id",
        Integer,
        ForeignKey("measurements.measurement_num_id"),
    ),
    Column(
        "sensor_measurement_num_id",
        Integer,
        ForeignKey("sensor_measurements.sensor_measurement_num_id"),
    ),
)


###############################################################################
# ORM data models
###############################################################################

class Topic(Base):
    """
    Represents a topic in the 'topics' table of the database.

    This class provides an ORM mapping for the 'topics' table, where each instance corresponds to a row in the table. It includes methods for adding new topics to the database.

    Attributes:
    - topic_num_id (int): The primary key of the topic.
    - topic (str): The name or title of the topic.

    Methods:
    - add(session, topic_to_add): Adds a new topic to the database.
    """
    __tablename__ = "topics"
    topic_num_id = Column(Integer, primary_key=True)
    topic = Column(String, unique=True)

    def add(self, session, topic_to_add):
        """
        Adds a new topic to the database if it doesn't already exist.

        This method checks if the given topic already exists in the database. If it doesn't, the method adds it.

        Parameters:
        - session (Session): The SQLAlchemy session for database operations.
        - topic_to_add (str): The name of the topic to be added.

        Returns:
        None
        """
        ic(f"Adding Topic: {topic_to_add}")
        topic = (
            session.query(Topic).filter_by(topic=topic_to_add).one_or_none()
        )
        if topic is not None:
            return
        session.add(Topic(topic=topic_to_add))
        session.commit()


class Sensor(Base):
    """
    Holds all of the sensors in the 'sensors' table of the database.

    This class provides an ORM mapping for the 'sensors' table, with methods to add new sensors to the database.

    Attributes:
    - sensor_num_id (int): The primary key of the sensor.
    - sensor_id (str): The unique identifier for the sensor.

    Methods:
    - add(session, sensor_to_add): Adds a new sensor to the database.
    """

    __tablename__ = "sensors"
    sensor_num_id = Column(Integer, primary_key=True)
    sensor_id = Column(String, unique=True)

    def add(self, session, sensor_to_add):
        """
        Adds a new sensor to the database if it doesn't already exist.

        This method checks if the given sensor already exists in the database. If not, it adds the new sensor.

        Parameters:
        - session (Session): The SQLAlchemy session for database operations.
        - sensor_to_add (str): The unique identifier of the sensor to be added.

        Returns:
        None
        """
        ic(f"Adding Sensor: {sensor_to_add}")
        existing_sensor = (
            session.query(Sensor).filter_by(sensor_id=sensor_to_add).one_or_none()
        )
        if existing_sensor is not None:
            return None
        session.add(Sensor(sensor_id=sensor_to_add))
        session.commit()


class Measurement(Base):
    """
    Represents a measurement type in the 'measurements' table of the database.

    This class provides an ORM mapping for the 'measurements' table. Each instance corresponds to a row in the table representing a type of measurement.

    Attributes:
    - measurement_num_id (int): The primary key of the measurement.
    - measurement (str): The name or description of the measurement kind.
    """
    """ "Create measurements table data model."""

    __tablename__ = "measurements"
    measurement_num_id = Column(Integer, primary_key=True)
    measurement = Column(String, unique=True)

    def add(self, session, measurement_to_add):
        """
        Adds a new measurement to the database if it doesn't already exist.

        This method checks if the given sensor already exists in the database. If not, it adds the new sensor.

        Parameters:
        - session (Session): The SQLAlchemy session for database operations.
        - sensor_to_add (str): The unique identifier of the sensor to be added.

        Returns:
        None
        """
        ic(f"Adding Sensor: {measurement_to_add}")
        measurement = (
            session.query(Measurement).filter_by(measurement=measurement_to_add).one_or_none()
        )
        if measurement is not None:
            return None
        session.add(Measurement(measurement=measurement_to_add))
        session.commit()

class SensorMeasurement(Base):
    """
    Represents a sensor measurement reading stored in the 'sensor_measurements' table of the database.

    This class provides an ORM mapping for the 'sensor_measurements' table. It includes relationships to the 'Topic', 'Sensor', and 'Measurement' classes and records various details about each sensor measurement.

    Attributes:
    - sensor_measurement_num_id (int): The primary key of the sensor measurement.
    - topic (relationship): The relationship to the 'Topic' class.
    - sensor (relationship): The relationship to the 'Sensor' class.
    - time (TIMESTAMP): The time at which the measurement was recorded.
    - measurement (relationship): The relationship to the 'Measurement' class.
    - value (float): The numerical value of the measurement.
    - value_2 (float): An additional numerical value for the measurement.
    - str_value (str): The string representation of the measurement value.

    Methods:
    - __repr__(): Returns a string representation of the sensor measurement instance.
    """

    __tablename__ = "sensor_measurements"
    sensor_measurement_num_id = Column(Integer, primary_key=True)

    topic = relationship(
        "Topic",
        secondary=topic_sensor_measurement,
        backref=backref("sensor_measurements"),
    )

    sensor = relationship(
        "Sensor",
        secondary=sensor_sensor_measurement,
        backref=backref("sensor_measurements"),
    )

    time = Column(TIMESTAMP(timezone=True), server_default=func.now())

    measurement = relationship(
        "Measurement",
        secondary=measurement_kind_sensor_measurement,
        backref=backref("sensor_measurements"),
    )

    value = Column(Float)
    value_2 = Column(Float)
    str_value = Column(String)

    def __repr__(self):
        """
        Returns a string representation of the SensorMeasurement instance.

        This method provides a convenient way to view the details of a sensor measurement, including its topic, sensor ID, time of measurement, measurement kind, and the values recorded.

        Returns:
        str: A string representation of the sensor measurement instance.
        """

        return (
            "topic: {}, sensor: {}, "
            "time: {}, "
            "measurement_kind: {}, "
            "measurement_value: {}".format(
                self.topic[0].topic,
                self.sensor[0].sensor_id,
                self.time.strftime("%Y-%m-%d %H:%M:%S"),
                self.measurement[0].measurement,
                self.value,
                self.value_2,
                self.str_value,
            )
        )


def initialize_sensor_data_db(fp="/home/beta/sensor_data.db"):
    """Initialize the database."""
    ic
    try:
        fp = Path(argv[1])
    except IndexError:
        print("No filepath provided. Using default filepath.")

    # with Path(fp) as sqlite_filepath:
    engine = ic(create_engine(f"sqlite:///{fp}"))

    Base.metadata.create_all(engine)

    Session = sessionmaker(engine)
    session = Session()
    session.commit()


if __name__ == "__main__":
    initialize_sensor_data_db("/home/beta/sensor_data.db")
