# ----------------------------------------------------------------------------
# Copyright (c) 2023, 4CSCC development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------


from paho-mqtt import client as mqtt

from mqtt_data_logger.callbacks import on_connect, on_message, log_sensor_data


def setUp():

    pass


def test_on_connect_fails_no_connection():
    assert on_connect()
