# functions to get cardinal direction and beaufort from wind speed and direction
master_map = {
    (0, 11.25): ('N', 0),
    (11.25, 33.75): ('NNE', 22.5),
    (33.75, 56.25): ('NE', 45),
    (56.25, 78.75): ('ENE', 67.5),
    (78.75, 101.25): ('E', 90),
    (101.25, 123.75): ('ESE', 112.5),
    (123.75, 146.25): ('SE', 135),
    (146.25, 168.75): ('SSE', 157.5),
    (168.75, 191.25): ('S', 180),
    (191.25, 213.75): ('SSW', 202.5),
    (213.75, 236.25): ('SW', 225),
    (236.25, 258.75): ('WSW', 247.5),
    (258.75, 281.25): ('W', 270),
    (281.25, 303.75): ('WNW', 292.5),
    (303.75, 326.25): ('NW', 315),
    (326.25, 348.75): ('NNW', 337.5),
    (348.75, 360): ('N', 0)
    }


def lookup_cardinal(angle):
    if not 0 <= angle < 360:
        raise ValueError(
            'Provided angle: ({}) not between 0 and 360'.format(angle))

    for cardinal_breaks in master_map.keys():
        if cardinal_breaks[0] <= angle < cardinal_breaks[1]:
            return master_map[cardinal_breaks]


beaufort_scale = [0, 1, 5, 11, 19, 28, 38, 49, 61, 74, 88, 102, 117, 999] 

beaufort_labels = ['Calm', 'Light Air', 'Light Breeze',
                   'Gentle Breeze', 'Moderate Breeze', 'Fresh Breeze',
                   'Strong Breeze', 'Near Gale', 'Gale', 'Strong Gale',
                   'Storm', 'Violent Storm', 'Hurricane Force']

beaufort_map = {
    (0, 1): 'Calm',
    (1, 5): 'Light Air',
    (5, 11): 'Light Breeze',
    (11, 19): 'Gentle Breeze',
    (19, 29): 'Moderate Breeze',
    (29, 38): 'Fresh Breeze',
    (38, 50): 'Strong Breeze',
    (50, 62): 'Near Gale',
    (62, 75): 'Gale',
    (75, 89): 'Strong Gale',
    (89, 103): 'Storm',
    (103, 118): 'Violent Storm',
    (118, 999): 'Hurricane Force'
    }


def lookup_beaufort(speed):
    if not isinstance(speed, (int, float)) or isinstance(speed, bool):
        raise TypeError(
            'Provided speed: ({}) not an integer or float'.format(speed))

    if not 0 <= speed < 999:
        raise ValueError(
            'Provided speed: ({}) not expected range: (0, 999)'.format(speed))

    for beaufort_breaks in beaufort_map.keys():
        if beaufort_breaks[0] <= speed < beaufort_breaks[1]: