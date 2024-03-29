import psycopg2
import player
import computer

class dbAdapter:

    conn = None
    cursor = None

    def __init__(self):
        try:
            self.conn = psycopg2.connect(dbname='postgres', user='postgres',password='', host='127.0.0.1',port=5432)
            self.cursor = self.conn.cursor()
            self.conn.rollback()
        except:
            pass

    def getUsers(self):
        self.cursor.execute('SELECT id FROM users')
        data = self.cursor.fetchall()
        self.conn.commit()
        self.cursor.execute('SELECT cash FROM users')
        dataCash = self.cursor.fetchall()
        self.conn.commit()
        return list(map(lambda x: x[0], data)), list(map(lambda x: x[0], dataCash))

    def getUserNames(self):
        self.cursor.execute('SELECT username FROM users')
        data = self.cursor.fetchall()
        return list(map(lambda x: x[0], data))

    def addUser(self,id,userName):
        self.cursor.execute('INSERT INTO users VALUES ({}, \'{}\', 0)'.format(id, userName))
        self.conn.commit()
        try:
            self.cursor.execute('CREATE TABLE computerSetup_{}(type TEXT, model TEXT, price INTEGER, perf INTEGER,'
                            ' activ INTEGER)'.format(id))
        except:
            pass
        self.conn.commit()


    def addCompomentDB(self,id,type,model,price,perf, activ):
        self.cursor.execute('INSERT INTO computerSetup_{} VALUES (\'{}\', \'{}\', {}, {}, {})'.format(id,type,model,price,perf, activ))
        self.conn.commit()

    def addCashDB(self, cash, id):
        self.cursor.execute('UPDATE users SET cash = {} WHERE id = {}'.format(cash, id))
        self.conn.commit()

    def sellInDB(self, id, model):
        self.cursor.execute('DELETE FROM computerSetup_{} WHERE model = \'{}\''.format(id, model))
        self.conn.commit()

    def deactivateInDB(self, id, model):
        self.cursor.execute('UPDATE computerSetup_{} SET activ = {} WHERE model = \'{}\''.format(id, 0, model))
        self.conn.commit()

    def activateInDB(self, id, model):
        self.cursor.execute('UPDATE computerSetup_{} SET activ = {} WHERE model = \'{}\''.format(id, 1, model))
        self.conn.commit()

    def startDB(self):

        players = dict()
        idList, cashList = self.getUsers()
        for id,cash in zip(idList, cashList):

            tempPlayer = player.player(id, cash)
            tempPlayer.computer = computer.computer()
            try:
                self.cursor.execute('SELECT * FROM computersetup_{}'.format(id))
                componentList = self.cursor.fetchall()
                motherboardDB = list(filter(lambda x: x[0] == "Материнская плата", componentList))

                motherboard = tempPlayer.menu.structure["Магазин"]["Материнская плата"][motherboardDB[0][1]]['Слоты']

                addCompResult = tempPlayer.computer.setMotherBoard(motherboard)
                for component in componentList:
                    if component[0] != "Материнская плата":
                        tempPlayer.computer.addComponent(component[0], component[1], component[2], component[3], component[4])
            except:
                self.conn.commit()

            players[id] = tempPlayer

        return players

    def iNeedMB(self, id):

        self.cursor.execute('SELECT model FROM computersetup_{} WHERE type = \'{}\''.format(id, "Материнская плата"))
        MB = self.cursor.fetchall()
        self.conn.commit()

        return MB[0][0]



    def showPC(self, id):
        description = ""
        tempPlayer = player.player(id, 0)
        try:
            stucker = 0
            self.cursor.execute('SELECT * FROM computersetup_{}'.format(id))
            componentList = self.cursor.fetchall()
            if len(componentList) == 0:
                description += "У вас ничего не куплено!"
            else:
                while stucker != len(componentList):
                    if componentList[stucker][0] == "Материнская плата":
                        motherboardDB = list(filter(lambda x: x[0] == "Материнская плата", componentList))
                        motherboard = tempPlayer.menu.structure["Магазин"]["Материнская плата"][motherboardDB[0][1]]['Слоты']
                        description += "Материнская плата: {}, Кол-во процессоров: {}, Кол-во слотов памяти: {}," \
                                       " Кол-во ЖД: {}, Кол-во видеокарт: {}\n\n".format(componentList[stucker][1],
                                                                                                  motherboard['Процессор'],
                                                                                                  motherboard['Память'],
                                                                                                  motherboard['Жесткий_диск'],
                                                                                                  motherboard['Видеокарта'],)
                        stucker += 1
                    else:
                        description += "{}: {}, Цена: {}, Производительность: {}, Активность (0 = выкл, 1 = вкл): {} \n\n".format(componentList[stucker][0],
                                                                                                                        componentList[stucker][1],
                                                                                                                        componentList[stucker][2],
                                                                                                                        componentList[stucker][3],
                                                                                                                        componentList[stucker][4])
                        stucker += 1
                a = 5
        except:
            pass
        return description

    def createTestData(self):
        try:
            self.addCompomentDB(111,"Процессор","afd","500","100")
            self.addCompomentDB(112, "Процессор", "afd", "500", "100")
            self.addCompomentDB(113, "Процессор", "afd", "500", "100")

            #self.addUser(111, "Lal")
            #self.addUser(112, "dad")
            #self.addUser(113, "fsdsa")

            #self.cursor.execute('INSERT INTO users (id) VALUES (1)')
            #self.cursor.execute('INSERT INTO users (id) VALUES (2)')
            #self.cursor.execute('INSERT INTO users (id) VALUES (3)')
        except:
            pass

        self.conn.commit()

    def db_init(self):
        try:
            self.cursor.execute('CREATE TABLE users(id INTEGER, userName TEXT, cash INTEGER)')

        except:
            pass

        self.conn.commit()

if __name__ == "__main__":

    db = dbAdapter()

    db.db_init()
    #db.createTestData()