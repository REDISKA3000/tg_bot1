import sqlite3


class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self,table):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute('SELECT cor, incor FROM {}'.format(table)).fetchall()

    def select_single(self, rownum):
        """ Получаем одну строку с номером rownum """
        with self.connection:
            return self.cursor.execute("SELECT * FROM mus WHERE id = ?", (rownum,)).fetchall()[0][3]

    @property
    def count_rows(self):
        """ Считаем количество строк """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM mus').fetchall()
            return len(result)

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()

    def create(self, user_id):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS stata(id INTEGER, cor INTEGER, incor INTEGER)')
        if not(user_id in self.cursor.execute('SELECT id FROM stata').fetchall()[:][0]):
            print(self.cursor.execute('SELECT id FROM stata').fetchall())
            self.cursor.execute('INSERT INTO stata (id,cor,incor) VALUES ({},0,0)'.format(user_id))
            self.cursor.execute('COMMIT')

    def update(self, user_id, c, b):
        self.cursor.execute('UPDATE stata SET cor = cor+{}, incor= incor + {} WHERE id == {} '.format(b,c,user_id))
        self.cursor.execute('COMMIT')
