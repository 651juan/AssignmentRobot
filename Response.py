from enum import Enum


class ResponseType(Enum):
    ASK = 1
    TELL = 2
    APPOINTMENT = 3
    CONFIRM = 4
    END = 5

class Response:
    def __init__(self, type='', value='', state_change=True):
        self.type = type
        self.value = value
        self.state_change = state_change
