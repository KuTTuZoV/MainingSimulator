import player

class computer:

    performance = 0

    slots = {}

    def addComponent(self, type, model, price, perf, active):
        try:
            #(None, None, None) = 0
            #(Athlon, None, None) = 1
            #(Athlon, Athlon, None) = 2
            #(Athlon, Athlon, Athlon) = -1

            index = self.slots[type].index(None)
            self.slots[type][self.slots[type].index(None)] = dict()

            self.slots[type][index]["Модель"]    = model
            self.slots[type][index]["Цена"]      = price
            self.slots[type][index]["Производительность"] = perf
            self.slots[type][index]["Активность"] = active
            #self.performance += perf
            return True
        except:
            return False

    def removeComponent(self, type, model):

        removeFlag = False
        index = 0

        for slot in self.slots[type]:
            if slot["Модель"] == model:
                self.slots[type][index] = None
                removeFlag = True
                break
            index += 1

        return removeFlag

    def deactivateComponent(self, type, model):

        removeFlag = False
        index = 0

        for slot in self.slots[type]:
            if slot["Модель"] == model:
                self.slots[type][index]['Активность'] = 0
                removeFlag = True
                break
            index += 1

        return removeFlag

    def activateComponent(self, type, model):

        removeFlag = False
        index = 0

        for slot in self.slots[type]:
            if slot["Модель"] == model:
                if self.slots[type][index]['Активность'] == 0:
                    self.slots[type][index]['Активность'] = 1
                    removeFlag = True
                    break
                else:
                    break
            index += 1

        return removeFlag

    #Удаление материнской платы
    #Проверка на наличие мат платы

    def setMotherBoard(self, motherBoardSlots):
        self.slots['Процессор']     = list([None] * motherBoardSlots['Процессор'])
        self.slots['Жесткий диск']  = list([None] * motherBoardSlots['Жесткий_диск'])
        self.slots['Видеокарта']    = list([None] * motherBoardSlots['Видеокарта'])
        self.slots['Память']        = list([None] * motherBoardSlots['Память'])

        return True

    def calculatePerformance(self):
        performance = 0

        for item in self.slots:
            for subitem in self.slots[item]:
                try:
                    if subitem["Активность"] == 1:
                        performance += int(subitem["Производительность"])
                except:
                    pass

        return performance

    def toString(self):
        description = ""

        for item in self.slots:
            for subitem in self.slots[item]:
                try:
                    description += "{}:{}:{}:{}:{}\n".format(item, subitem["Модель"], subitem["Цена"], subitem["Производительность"], subitem["Активность"])
                except:
                    description += "{}:{}\n".format(item, "свободен")

        return description
    def __init__(self):
        self.slots = {
            "Процессор": list(),
            "Жесткий диск": list(),
            "Видеокарта": list(),
            "Память": list(),
        }

if __name__ == "__main__":

    tempPlayer = player.player(1,1500)
    tempComputer = computer()

    motherboard = tempPlayer.menu.structure["Магазин"]["Материнская плата"]["AsRock"]['Слоты']
    tempComputer.setMotherBoard(motherboard)
    tempComputer.addComponent("Процессор", "Athlon",1000, 100, 1)
    tempComputer.addComponent("Процессор", "Athlon",1000, 100, 0)

    tempComputer.calculatePerformance()

    pass