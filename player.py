import computer
import menu
import json

class EventHook(object):
    def __init__(self):
        self.__handlers = []

    def __iadd__(self, handler):
        self.handlers.append(handler)
        return self

    def __isub__(self, handler):
        self.handlers.remove(handler)
        return self

    def fire(self, *args, **keywargs):
        for handler in self.__handlers:
            handler(*args, **keywargs)

class player:
    computer = computer.computer()
    menu = menu.menu()
    hints    = None

    def __init__(self):
        self.hints = list(json.loads(open("hints", encoding="utf-8-sig").read()))
        self.onPayDay = EventHook()

if __name__ == "__main__":

    player = player()
