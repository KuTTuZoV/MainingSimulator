import computer
import menu
import json

class player():
    computer = computer.computer()
    menu = menu.menu()
    hints    = None
    cash = 1500
    id = 0

    def calculateCash(self):
        self.cash += self.computer.calculatePerformance()
        return self.cash

    def __init__(self, id, cash):
        super().__init__()

        hintsData = json.loads(open("hints", encoding="utf-8-sig").read())
        hintKeys  = list(hintsData)
        self.hints = list()
        self.id = id
        self.cash = cash
        for key in hintKeys:
            self.hints.append(key + " : " + hintsData[key])

if __name__ == "__main__":

    player = player(1000)

    while True:
        pass
