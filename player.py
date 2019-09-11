import computer
import menu
import json

class player():
    computers = list()
    menu = menu.menu()
    hints    = None
    cash = 1500
    id = 0

    components = list()

    def showComponents(self):
        pass

    def calculateCash(self):
        self.cash += self.computer.calculatePerformance()
        return self.cash

    def setMotherboard(self, motherBoardSlots, compability, computerNumber):
        return self.computers[computerNumber].setMotherBoard(motherBoardSlots, compability)

    def addMotherboard(self, motherBoardSlots, compability):
        self.computers.append(computer.computer())
        return self.computers[-1].setMotherBoard(motherBoardSlots, compability)

    def addComponent(self, type, model, price, perf, active, level, computerNumber):

        if computerNumber < len(self.computers):

            res = self.computers[computerNumber].addComponent(type, model, price, perf, active, level)

            if res[0] == True:
                self.components.append([type, model, price, perf, active, level, computerNumber])

            return res

        else:
            return [False, "Нет материнской платы!"]

    def removeComponent(self, componentIndex):

        if componentIndex < len(self.components):

            if self.components[componentIndex][4] == 1:
                computerNumber = self.components[componentIndex][6]
                model          = self.components[componentIndex][1]
                type           = self.components[componentIndex][0]
            else:
                return False, "Компонент уже извлечен!"

            self.deactivateComponent(componentIndex)
            return self.computers[computerNumber].removeComponent(type, model)
        else:
            return False, "Индекс выходит за пределы!"

    def activateComponent(self, componentIndex):
        computerNumber = self.components[componentIndex][6]
        model          = self.components[componentIndex][1]
        type           = self.components[componentIndex][0]

        self.computers[computerNumber].activateComponent(type, model)

    def deactivateComponent(self, componentIndex):
        computerNumber = self.components[componentIndex][6]
        model          = self.components[componentIndex][1]
        type           = self.components[componentIndex][0]

        self.components[componentIndex][4] = 0
        self.computers[computerNumber].deactivateComponent(type, model)

    def sellComponent(self, componentIndex):

        if componentIndex < len(self.components):

            computerNumber = self.components[componentIndex][6]
            model = self.components[componentIndex][1]
            type = self.components[componentIndex][0]

            self.components.pop(componentIndex)
            self.computers[computerNumber].deactivateComponent(type, model)

            return True, "Компонент продан!"

        else:
            return False, "Индекс выходит за пределы!"

    def removeMotherboard(self, computerNumber):
        self.computers.pop(computerNumber)

        for component in self.components:
            component[4] = 0
            component[6] = -1


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
