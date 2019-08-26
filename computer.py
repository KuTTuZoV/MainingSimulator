class computer:

    performance = 0

    slots = {
        "Процессор"    : list(),
        "Жесткий диск" : list(),
        "Видеокарта"    : list(),
        "Память"        : list(),
    }

    def addComponent(self, type, model, perf):
        try:
            #(None, None, None) = 0
            #(Athlon, None, None) = 1
            #(Athlon, Athlon, None) = 2
            #(Athlon, Athlon, Athlon) = -1

            self.slots[type][self.slots[type].index(None)] = model
            self.performance += perf
            return True
        except:
            return False

    def removeComponent(self, type, slotNumber):
        self.slots[type][slotNumber] = None

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
                    performance += int(subitem["Производительность"])
                except:
                    pass

        return performance

    def toString(self):
        description = ""

        for item in self.slots:
            for subitem in self.slots[item]:
                try:
                    description += "{}:{}\n".format(item, subitem["Модель"])
                except:
                    description += "{}:{}\n".format(item, "свободен")

        return description
    def __init__(self):
        pass