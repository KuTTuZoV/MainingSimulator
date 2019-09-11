import player
import json
import DB_init
import unittest

assortment = json.loads(open("assortment",encoding="utf-8-sig").read())
dbAdapter = DB_init.dbAdapter()

pl = {}

pl[1234] = player.player(111, 1500)

def addMotherboard(id, model):
    motherboard = assortment["Материнская плата"][model]

    if pl[id].computer.setMotherBoard(motherboard["Слоты"], motherboard["Совместимость"]):
        dbAdapter.addMotherboard(id, 1, "Материнская плата", model, motherboard["Цена"], motherboard["Производительность"], 1)
        return True

    return False

def addComponent(id, mbid, type, model):
    component = assortment[type][model]

    res =  pl[id].computer.addComponent(type, model, component['Цена'], component['Производительность'], 1, component['Уровень'])

    if res[0]:
        dbAdapter.addCompomentDB(id, type, model, component["Цена"],
                                 component["Производительность"], 1, component["Уровень"], mbid)
    return res

class TestStringMethods(unittest.TestCase):

    def test_01_delUser(self):
        dbAdapter.delUser(1234)

    def test_02_addUser(self):

        try:
            dbAdapter.addUser(1234, "TestUser")
        except:
            dbAdapter.conn.commit()

        result = dbAdapter.getUsers()

        self.assertTrue(1234 in result[0])

    def test_03_addProcessorWithoutMotherboad(self):

        type  = 'Процессор'
        model = 'AMD Athlon'
        id    = 1234
        mbid  = 1

        component = assortment[type][model]

        res = pl[id].addComponent(type, model, component['Цена'], component['Производительность'], 1,
                                           component['Уровень'], computerNumber=0)

        if res[0]:
            dbAdapter.addCompomentDB(id, type, model, component["Цена"],
                                     component["Производительность"], 1, component["Уровень"], mbid)

        self.assertFalse(res[0])
        self.assertEqual(res[1], "Нет материнской платы!")
        components = dbAdapter.getUserComponents(1234)

        self.assertEqual(len(components), 0)

    def test_04_addMotherboard(self):
        model = "AsRock"
        id    = 1234

        motherboard = assortment["Материнская плата"][model]

        res = pl[id].addMotherboard(motherboard["Слоты"], motherboard["Совместимость"])

        if res:
            dbAdapter.addMotherboard(id, 1, "Материнская плата", model, motherboard["Цена"],
                                     motherboard["Производительность"], 1)

        self.assertTrue(res)

        motherboards = dbAdapter.getUserMotherboards(1234)

        self.assertEqual(motherboards[0][2], "AsRock")

    def test_05_addComponent(self):
        type = 'Процессор'
        model = 'AMD Athlon'
        id = 1234
        mbid = 0

        component = assortment[type][model]

        res = pl[id].addComponent(type, model, component['Цена'], component['Производительность'], 1,
                                  component['Уровень'], computerNumber=mbid)

        if res[0]:
            dbAdapter.addCompomentDB(id, type, model, component["Цена"],
                                     component["Производительность"], 1, component["Уровень"], mbid)

        self.assertEqual(res[1], "Компонент установлен!")
        components = dbAdapter.getUserComponents(1234)

        self.assertEqual(len(components), 1)
        self.assertEqual(components[0][0], 'Процессор')
        self.assertEqual(components[0][1], 'AMD Athlon')

    def test_06_addComponent(self):
        type = 'Процессор'
        model = 'AMD Athlon'
        id = 1234
        mbid = 0

        component = assortment[type][model]

        res = pl[id].addComponent(type, model, component['Цена'], component['Производительность'], 1,
                                  component['Уровень'], computerNumber=mbid)

        if res[0]:
            dbAdapter.addCompomentDB(id, type, model, component["Цена"],
                                     component["Производительность"], 1, component["Уровень"], mbid)

        self.assertEqual(res[1], "Компонент установлен!")
        components = dbAdapter.getUserComponents(1234)

        self.assertEqual(len(components), 2)

        self.assertEqual(components[0][0], 'Процессор')
        self.assertEqual(components[0][1], 'AMD Athlon')

        self.assertEqual(components[1][0], 'Процессор')
        self.assertEqual(components[1][1], 'AMD Athlon')

    def test_07_addOverComponent(self):
        type = 'Процессор'
        model = 'AMD Athlon'
        id = 1234
        mbid = 0

        component = assortment[type][model]

        res = pl[id].addComponent(type, model, component['Цена'], component['Производительность'], 1,
                                  component['Уровень'], computerNumber=mbid)

        if res[0]:
            dbAdapter.addCompomentDB(id, type, model, component["Цена"],
                                     component["Производительность"], 1, component["Уровень"], mbid)

        self.assertEqual(res[1], "Нет свободных слотов")

        self.assertEqual(len(pl[id].components), 2)

        components = dbAdapter.getUserComponents(1234)

        self.assertEqual(len(components), 2)

        self.assertEqual(components[0][0], 'Процессор')
        self.assertEqual(components[0][1], 'AMD Athlon')

        self.assertEqual(components[1][0], 'Процессор')
        self.assertEqual(components[1][1], 'AMD Athlon')

    def test_08_removeComponent1(self):
        type = 'Процессор'
        model = 'AMD Athlon'
        id = 1234
        mbid = 0

        component = assortment[type][model]

        res = pl[id].removeComponent(0)

        if res[0]:
            dbAdapter.deactivateInDB(id, model, mbid)

        components = dbAdapter.getUserComponents(1234)

        self.assertEqual(len(components), 2)

        self.assertEqual(components[0][0], 'Процессор')
        self.assertEqual(components[0][1], 'AMD Athlon')
        self.assertEqual(components[0][4], 1)

        self.assertEqual(components[1][0], 'Процессор')
        self.assertEqual(components[1][1], 'AMD Athlon')
        self.assertEqual(components[1][4], 0)

    def test_09_removeRemovedComponent(self):
        type = 'Процессор'
        model = 'AMD Athlon'
        id = 1234
        mbid = 0

        component = assortment[type][model]

        res = pl[id].removeComponent(0)

        self.assertEqual(len(pl[id].components), 2)

        self.assertFalse(res[0])
        self.assertEqual(res[1], "Компонент уже извлечен!")

        components = dbAdapter.getUserComponents(1234)

        self.assertEqual(len(components), 2)

        self.assertEqual(components[0][0], 'Процессор')
        self.assertEqual(components[0][1], 'AMD Athlon')
        self.assertEqual(components[0][4], 1)

        self.assertEqual(components[1][0], 'Процессор')
        self.assertEqual(components[1][1], 'AMD Athlon')
        self.assertEqual(components[1][4], 0)

    def test_10_removeComponent2(self):
        type = 'Процессор'
        model = 'AMD Athlon'
        id = 1234
        mbid = 0

        component = assortment[type][model]

        res = pl[id].removeComponent(1)

        if res[0]:
            dbAdapter.deactivateInDB(id, model, mbid)

        components = dbAdapter.getUserComponents(1234)

        self.assertEqual(len(components), 2)

        self.assertEqual(components[0][0], 'Процессор')
        self.assertEqual(components[0][1], 'AMD Athlon')
        self.assertEqual(components[0][4], 0)

        self.assertEqual(components[1][0], 'Процессор')
        self.assertEqual(components[1][1], 'AMD Athlon')
        self.assertEqual(components[1][4], 0)

    def test_11_sellOverComponent1(self):
        type = 'Процессор'
        model = 'AMD Athlon'
        id = 1234
        mbid = 0

        component = assortment[type][model]

        res = pl[id].sellComponent(3)

        self.assertEqual(len(pl[id].components), 2)
        self.assertFalse(res[0])

        components = dbAdapter.getUserComponents(1234)

        self.assertEqual(len(components), 2)

        self.assertEqual(components[0][0], 'Процессор')
        self.assertEqual(components[0][1], 'AMD Athlon')
        self.assertEqual(components[0][4], 0)

    def test_12_sellComponent1(self):
        type = 'Процессор'
        model = 'AMD Athlon'
        id = 1234
        mbid = 0

        component = assortment[type][model]

        res = pl[id].sellComponent(0)

        if res[0]:
            dbAdapter.sellInDB(id, model, mbid)

        components = dbAdapter.getUserComponents(1234)

        self.assertEqual(len(components), 1)

        self.assertEqual(components[0][0], 'Процессор')
        self.assertEqual(components[0][1], 'AMD Athlon')
        self.assertEqual(components[0][4], 0)

    def test_13_sellComponent2(self):
        type = 'Процессор'
        model = 'AMD Athlon'
        id = 1234
        mbid = 0

        component = assortment[type][model]

        res = pl[id].sellComponent(0)

        if res[0]:
            dbAdapter.sellInDB(id, model, mbid)

        components = dbAdapter.getUserComponents(1234)

        self.assertEqual(len(components), 0)

    def test_14_removeMotherboard(self):
        id = 1234
        mbid = 0

        type = 'Процессор'
        model = 'AMD Athlon'
        id = 1234
        mbid = 0

        component = assortment[type][model]

        pl[id].addComponent(type, model, component['Цена'], component['Производительность'], 1,
                                  component['Уровень'], computerNumber=mbid)

        pl[id].addComponent(type, model, component['Цена'], component['Производительность'], 1,
                                  component['Уровень'], computerNumber=mbid)

        res = pl[id].removeMotherboard(0)


if __name__ == '__main__':
    unittest.main()