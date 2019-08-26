import computer
import menu
import json
import threading

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal, QObject, QTimer


class player(QObject):
    paydaySignal = pyqtSignal(int, float)

    timer = threading.Timer

    computer = computer.computer()
    menu = menu.menu()
    hints    = None
    cash = 1500
    id = 0


    def payday(self):
        self.cash += self.computer.performance
        self.paydaySignal.emit(self.id, self.cash)

    def __init__(self, id):
        super().__init__()
        QTimer().__init__()

        hintsData = json.loads(open("hints", encoding="utf-8-sig").read())
        hintKeys  = list(hintsData)
        self.hints = list()
        self.id = id

        self.timer = threading.Timer(1, self.payday)
        self.timer.start()

        for key in hintKeys:
            self.hints.append(key + " : " + hintsData[key])

if __name__ == "__main__":

    player = player(1000)

    while True:
        pass
