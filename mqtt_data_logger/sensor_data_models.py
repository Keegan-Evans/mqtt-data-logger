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
    """Create a topic table data model."""

    __tablename__ = "topics"
    topic_num_id = Column(Integer, primary_key=True)
    topic = Column(String, unique=True)

    def add(self, session, topic_to_add):
        """Add a new topic to the database."""
        topic = (
            session.query(Topic).filter_by(topic=topic_to_add).one_or_none()
        )
        if topic is None:
            return
        session.add(Topic(topic=topic_to_add))
        session.commit()


class Sensor(Base):
    """Create sensors table data model."""

    __tablename__ = "sensors"
    sensor_num_id = Column(Integer, primary_key=True)
    sensor_id = Column(String, unique=True)

    def add(self, session, sensor_to_add):
        """Add a new sensor to the database."""
        sensor = (
            session.query(Sensor).filter_by(sensor=sensor_to_add).one_or_none()
        )
        if sensor is None:
            return
        session.add(Sensor(sensor=sensor_to_add))
        session.commit()


class Measurement(Base):
    """ "Create measurements table data model."""

    __tablename__ = "measurements"
    measurement_num_id = Column(Integer, primary_key=True)
    measurement = Column(String, unique=True)


class SensorMeasurement(Base):
    """Create sensor measurements table data model."""

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

    time = Column(DateTime(timezone=True), server_default=func.now())

    measurement = relationship(
        "Measurement",
        secondary=measurement_kind_sensor_measurement,
        backref=backref("sensor_measurements"),
    )

    value = Column(Float)

    def __repr__(self):
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
            )
        )


def initialize_sensor_data_db(fp):
    """Initialize the database."""
    with Path(fp) as sqlite_filepath:
        engine = create_engine(f"sqlite:///{sqlite_filepath}")

    Base.metadata.create_all(engine)

    Session = sessionmaker(engine)
    session = Session()
    session.commit()


if __name__ == "__main__":
    initialize_sensor_data_db("/home/beta/sensor_data.db")
