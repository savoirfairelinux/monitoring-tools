
from collections import namedtuple

States = namedtuple('States', 'OK, WARNING, CRITICAL, UNKNOWN')

STATES = States(0, 1, 2, 3)

STATES_2_NAME = {
    STATES.OK:          'OK',
    STATES.WARNING:     'WARNING',
    STATES.CRITICAL:    'CRITICAL',
    STATES.UNKNOWN:     'UNKNOWN',
}

