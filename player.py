import computer
import menu
import json

class player:
    computer = computer.computer()
    menu = menu.menu()
    hints    = None

    def __init__(self):
        self.hints = list(json.loads(open("hints", encoding="utf-8-sig").read()))

if __name__ == "__main__":

    player = player()
