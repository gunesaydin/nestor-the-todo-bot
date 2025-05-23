from enum import Enum

class CommandType(Enum):
    NONE = "NONE"
    START = "START"
    HELP = "HELP"
    ADD = "ADD"
    REMOVE = "REMOVE"
    INSERT = "INSERT"
    LIST = "LIST"
    WHATNOW = "WHATNOW"
    DONE = "DONE"
    CLEAR = "CLEAR"

class Command():
    def __init__(self, value:str):
        super().__init__()
        self.type = self.parse(value)
        
    def parse(self, value:str) -> CommandType:
        try:
            if value == "/start":
                return CommandType.START
            elif value == "/help":
                return CommandType.HELP
            elif value == "/add":
                return CommandType.ADD
            elif value == "/remove":
                return CommandType.REMOVE
            elif value == "/insert":
                return CommandType.INSERT
            elif value == "/list":
                return CommandType.LIST
            elif value == "/whatnow":
                return CommandType.WHATNOW
            elif value == "/done":
                return CommandType.DONE
            elif value == "/clear":
                return CommandType.CLEAR
            else:
                return CommandType.NONE
        except KeyError:
            raise ValueError(f"Invalid request type: {value}")