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

# dbAdapter.delUser(1234)
# dbAdapter.addUser(1234, "testUser")
#
# try:
#     addMotherboard(1234, "AsRock")
# except:
#     pass
#
# res = addComponent(1234, 1, "Процессор", "AMD Athlon")
# print(res[1])
#
# res = addComponent(1234, 1, "Процессор", "AMD Athlon")
# print(res[1])
#
# res = addComponent(1234, 1, "Процессор", "AMD Athlon")
# print(res[1])
#
# players = dbAdapter.startDB()


class TestStringMethods(unittest.TestCase):

    def test_clearDB(self):
        tables = dbAdapter.getTables()

        if tables is not None:
            for table in tables:
                dbAdapter.dropTable(table)

        tables = dbAdapter.getTables()

        self.assertEqual(len(tables), 0)

    def test_dbInit(self):
        dbAdapter.db_init()

    def test_addUser(self):
        dbAdapter.addUser(1234, "TestUser")
        result = dbAdapter.getUsers()

        self.assertTrue(1234 in result)

    #def test_delUser(self):
    #    dbAdapter.delUser(1234)

if __name__ == '__main__':
    unittest.main()