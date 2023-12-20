# import pytest
from importlib import metadata
# import inspect
from tkinter import W
import unittest
from icecream import ic
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from mqtt_data_logger.sensor_data_models import (
    Base, Topic, Sensor, Measurement, SensorMeasurement,
    initialize_sensor_data_db
)
import os

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

class TestSensorData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create an SQLite in-memory database and apply the schema
        # ic(initialize_sensor_data_db(TEST_DATABASE_FP))
        cls.engine = create_engine(TEST_DATABASE_URL)
        Base.metadata.create_all(cls.engine)

    @classmethod
    def tearDownClass(cls):
        # Clean up: drop the database tables at the end of the session
        Base.metadata.drop_all(cls.engine)

    def setUp(self):
        # Create a session to interact with the database
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Populate the database with test data if needed
        # Example: Add test data for a topic
        # test_topic = Topic(topic="TestTopic")
        # self.session.add(test_topic)
        # self.session.commit()

    def tearDown(self):
        # Clean up: close the session at the end of each test function
        self.session.close()

    def test_database_initilization(self):
        ic()
        # Call the initialize_sensor_data_db function

        # Check if tables exist in the database
        tables = ic([i for i in Base.metadata.tables.keys()])

        # Assert that all required tables are present
        self.assertIn("topics", tables)
        self.assertIn("sensors", tables)
        self.assertIn("measurements", tables)
        self.assertIn("sensor_measurements", tables)
        # ancillary/mapping tables
        self.assertIn("topic_sensor_measurement", tables)
        self.assertIn("sensor_sensor_measurement", tables)
        self.assertIn("measurement_kind_sensor_measurement", tables)

    def test_add_new_topic(self):
        ic()
        """ Test adding a new topic. """
        topic_name = "Test Topic"
        new_topic = Topic(topic=topic_name)
        new_topic.add(self.session, topic_name)
        
        added_topic = ic(self.session.query(Topic).filter_by(topic=topic_name).first())
        self.assertIsNotNone(added_topic)
        self.assertEqual(added_topic.topic, topic_name)

    def test_add_existing_topic(self):
        """ Test adding an existing topic. """
        topic_name = "Test Topic"
        new_topic = Topic()
        new_topic.add(self.session, topic_name)
        
        # Try to add the same topic again
        new_topic.add(self.session, topic_name)

        topics_count = self.session.query(Topic).filter_by(topic=topic_name).count()
        self.assertEqual(topics_count, 1)  # Should still be only one topic with this name

    # sensor table
    def test_add_new_sensor(self):
        """ Test adding a new sensor. """
        ic()
        sensor = "Sensor123"
        new_sensor = Sensor()
        new_sensor.add(self.session, sensor)

        added_sensor = self.session.query(Sensor).filter_by(sensor_id=sensor).first()
        self.assertIsNotNone(added_sensor)
        self.assertEqual(added_sensor.sensor_id, sensor)

    def test_add_existing_sensor(self):
        ic()
        """ Test adding an existing sensor. """
        sensor = "Sensor123"
        new_sensor = Sensor()
        new_sensor.add(self.session, sensor)

        # Try to add the same sensor again
        new_sensor.add(self.session, sensor)

        sensors_count = ic(self.session.query(Sensor).filter_by(sensor_id=sensor).count())
        self.assertEqual(sensors_count, 1)  # Should still be only one sensor with this ID


    # measurement table
    def test_add_new_measurement(self):
        """ Test adding a new measurement. """
        ic()
        measurement = "measurement123"
        new_measurement = Measurement()
        new_measurement.add(self.session, measurement)

        added_measurement = self.session.query(Measurement).filter_by(measurement=measurement).first()
        self.assertIsNotNone(added_measurement)
        self.assertEqual(added_measurement.measurement, measurement)

    def test_add_existing_measurement(self):
        ic()
        """ Test adding an existing measurement. """
        measurement = "measurement123"
        Measurement().add(self.session, measurement)
        new_measurement = Measurement()
        new_measurement.add(self.session, measurement)

        # Try to add the same measurement again
        new_measurement.add(self.session, measurement)

        measurements_count = ic(self.session.query(Measurement).filter_by(measurement=measurement).count())
        self.assertEqual(measurements_count, 1)  # Should still be only one measurement with this ID

    def test_sensor_measurement_repr(self):
        """ Test the string representation of SensorMeasurement. """
        topic = Topic(topic="Environment")
        sensor = Sensor(sensor_id="EnvSensor01")
        measurement = Measurement(measurement="Temperature")
        sensor_measurement = SensorMeasurement(
            topic=[topic],
            sensor=[sensor],
            measurement=[measurement],
            value=23.5,
            value_2=24.0,
            str_value="23.5°C"
        )
        self.session.add_all([topic, sensor, measurement, sensor_measurement])
        self.session.commit()

        retrieved_measurement = self.session.query(SensorMeasurement).first()
        expected_repr = "topic: Environment, sensor: EnvSensor01, time: {}, measurement_kind: Temperature, measurement_value: 23.5".format(retrieved_measurement.time.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(retrieved_measurement.__repr__(), expected_repr)



if __name__ == "__main__":
    unittest.main()
# 
# @pytest.fixture(scope="session")
# def db_engine(request):
#     Create an SQLite in-memory database and apply the schema
#     engine = create_engine(TEST_DATABASE_URL)
#     Base.metadata.create_all(engine)

#     def cleanup():
#         # Clean up: drop the database tables at the end of the session
#         # Base.metadata.drop_all(engine)
#         pass

#     # Register the cleanup function to be called at the end of the session
#     request.addfinalizer(cleanup)

#     return engine

# @pytest.fixture(scope="function", autouse=True)
# def db_session(db_engine, request):
#     # Create a session to interact with the database
#     Session = sessionmaker(bind=db_engine)
#     session = Session()

#     # Populate the database with test data if needed
#     # Example: Add test data for a topic
#     # test_topic = Topic(topic="TestTopic")
#     # session.add(test_topic)
#     # session.commit()

#     def cleanup():
#         # Clean up: close the session at the end of each test function
#         session.close()

#     # Register the cleanup function to be called at the end of each test function
#     request.addfinalizer(cleanup)

#     return session

# @pytest.fixture(autouse=True)
# def setup_teardown():
#     # Setup: code to be executed before each test
#     print("\nSetup: This will run before each test")

#     yield  # This is the equivalent of the "teardown" part

#     # Teardown: code to be executed after each test
#     print("\nTeardown: This will run after each test")

# def test_topic_add(db_session):
#     ic(session)
#     assert False
#     # Test the add method of the Topic class
#     topic_name = "TestTopic"
#     new_topic = Topic()
#     new_topic.add(db_session, topic_name)

#     db_session.commit()

#     # Query the database to check if the topic was added successfully
#     added_topic = db_session.query(Topic).filter_by(topic=topic_name).first()
#     assert added_topic is not None
#     assert added_topic.topic == topic_name

# Add more test functions for other classes and methods as needed


# @pytest.fixture
# def db_session():
    # Create an SQLite in-memory database and apply the schema
    # engine = create_engine(TEST_DATABASE_FP)
    # Base.metadata.create_all(engine)
    
    # Create a session to interact with the database
    # Session = sessionmaker(bind=engine)
    # session = Session()

    # Populate the database with test data if needed
    # Example: Add test data for a topic
    # test_topic = Topic(topic="TestTopic")
    # session.add(test_topic)
    # session.commit()

    # yield session

    # Clean up: close the session and drop the database tables
    # session.close()
    # Base.metadata.drop_all(engine)

# def test_topic_add(db_session):
    # Test the add method of the Topic class
    # topic_name = "NewTopic"
    # new_topic = Topic()
    # new_topic.add(db_session, topic_name)

    # Query the database to check if the topic was added successfully
    # added_topic = db_session.query(Topic).filter_by(topic=topic_name).first()
    # assert added_topic is not None
    # assert added_topic.topic == topic_name

# Add more test functions for other classes and methods as needed

# Example of a test function for the Sensor class
# def test_sensor_add(db_session):
    # sensor_id = "NewSensor"
    # new_sensor = Sensor()
    # new_sensor.add(db_session, sensor_id)

    # added_sensor = db_session.query(Sensor).filter_by(sensor=sensor_id).first()
    # assert added_sensor is not None
    # assert added_sensor.sensor == sensor_id

# @pytest.fixture
# def db_cleanup(db_session):
    # Clean up: close the session and drop the database tables
    # db_session.close()
    # Base.metadata.drop_all(db_session.bind)