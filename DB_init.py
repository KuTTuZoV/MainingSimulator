import psycopg2

class dbAdapter:

    conn = None
    cursor = None

    def __init__(self):
        try:
            self.conn = psycopg2.connect(dbname='postgres', user='postgres',password='', host='127.0.0.1',port=5432)
            self.cursor = self.conn.cursor()
        except:
            pass

    def getUsers(self):
        self.cursor.execute('SELECT id FROM users')
        data = self.cursor.fetchall()
        return list(map(lambda x: x[0], data))

    def getUserNames(self):
        self.cursor.execute('SELECT username FROM users')
        data = self.cursor.fetchall()
        return list(map(lambda x: x[0], data))

    def addUser(self,id,userName):
        self.cursor.execute('INSERT INTO users VALUES ({}, \'{}\', 0)'.format(id, userName))
        self.conn.commit()

    def createTestData(self):
        try:
            self.cursor.execute('INSERT INTO users (id) VALUES (1)')
            self.cursor.execute('INSERT INTO users (id) VALUES (2)')
            self.cursor.execute('INSERT INTO users (id) VALUES (3)')
        except:
            pass

        self.conn.commit()

    def db_init(self):
        try:
            self.cursor.execute('CREATE TABLE users(id INTEGER, userName TEXT, cash INTEGER)')

        except:
            pass

        self.conn.commit()