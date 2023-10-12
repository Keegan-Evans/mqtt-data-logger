# ----------------------------------------------------------------------------
# Copyright (c) 2023, 4CSCC development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------


from mqtt_data_logger.util import start_session, get_mqtt_client

from pathlib import Path


def main():
    session = start_session(Path("/home/beta/sensor_data.db"))

    client = get_mqtt_client()

    client.loop_forever()
