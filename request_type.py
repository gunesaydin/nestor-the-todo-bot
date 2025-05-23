from enum import Enum

class RequestType(Enum):
    START = "START"
    HELP = "HELP"
    SETTINGS = "SETTINGS"
    ADD = "ADD"
    LIST = "LIST"
    WHATNOW = "WHATNOW"
    DONE = "DONE"
    CLEAR = "CLEAR"