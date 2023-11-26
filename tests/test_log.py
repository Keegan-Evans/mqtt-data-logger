from py import test
# from mqtt_data_logger.log_data import add_sensors_reading_record
from mqtt_data_logger.munge_wind import lookup_cardinal, lookup_beaufort
import unittest
import json
import pytest


class TestWindLogging(unittest.TestCase):
    def setUp(self):
        pass
        # self.test_data = json.dumps({})

    def test_cardinal_binning(self):

        # For South
        # lower bound
        assert lookup_cardinal(168.75)[0] == 'S' != 'SSE' != 'SSW'
        assert lookup_cardinal(168.75)[1] == 180
        # middle of range
        assert lookup_cardinal(180)[0] == 'S' != 'SSE' != 'SSW'
        assert lookup_cardinal(180)[1] == 180
        # upper bound
        assert lookup_cardinal(191.25)[0] == 'SSW' != 'SSE' != 'S'
        assert lookup_cardinal(191.25)[1] == 202.5
        # assert lookup_cardinal((180 + 12.25)) == 'S' != 'SSW'

        # For East North East
        # lower bound
        assert lookup_cardinal(56.25)[0] == 'ENE' != 'NE' != 'E'
        assert lookup_cardinal(56.25)[1] == 67.5
        # middle of range
        assert lookup_cardinal(67.5)[0] == 'ENE' != 'NE' != 'E'
        assert lookup_cardinal(67.5)[1] == 67.5
        # upper bound
        assert lookup_cardinal(78.75)[0] == 'E' != 'NE' != 'ENE'
        assert lookup_cardinal(78.75)[1] == 90

    def test_beaufort_binning(self):
        assert lookup_beaufort(0) == 'Calm'
        assert lookup_beaufort(0.5) == 'Calm'
        assert lookup_beaufort(1) == 'Light Air'
        assert lookup_beaufort(3) == 'Light Air'
        assert lookup_beaufort(5) == 'Light Breeze'
        assert lookup_beaufort(11) == 'Gentle Breeze'
        assert lookup_beaufort(19) == 'Moderate Breeze'
        assert lookup_beaufort(29) == 'Fresh Breeze'
        assert lookup_beaufort(38) == 'Strong Breeze'
        assert lookup_beaufort(49) == 'Strong Breeze'
        assert lookup_beaufort(50) == 'Near Gale'
        assert lookup_beaufort(61) == 'Near Gale'
        assert lookup_beaufort(62) == 'Gale'
        assert lookup_beaufort(74) == 'Gale'
        assert lookup_beaufort(75) == 'Strong Gale'
        assert lookup_beaufort(88) == 'Strong Gale'
        assert lookup_beaufort(89) == 'Storm'
        assert lookup_beaufort(102) == 'Storm'
        assert lookup_beaufort(103) == 'Violent Storm'
        assert lookup_beaufort(117) == 'Violent Storm'
        assert lookup_beaufort(118) == 'Hurricane Force'

    def test_beaufort_binning_fails_on_non_numeric_input(self):
        with pytest.raises(TypeError):
            lookup_beaufort('a')
        with pytest.raises(TypeError):
            lookup_beaufort('1')
        with pytest.raises(TypeError):
            lookup_beaufort([1, 2, 3])
        with pytest.raises(TypeError):
            lookup_beaufort({'a': 1, 'b': 2})
        with pytest.raises(TypeError):
            lookup_beaufort((1, 2, 3))
        with pytest.raises(TypeError):
            lookup_beaufort(None)
        with pytest.raises(TypeError):
            lookup_beaufort(True)
        with pytest.raises(TypeError):
            lookup_beaufort(False)
        with pytest.raises(TypeError):
            lookup_beaufort({'a', 'b', 'c'})
        with pytest.raises(TypeError):
            lookup_beaufort({'a': 1, 'b': 2, 'c': 3})
