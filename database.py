import sqlite3
from PIL import Image

class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self, table):
        """ Получаем все строки выбранной таблицы"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM {}'.format(table)).fetchall()

    def select_single(self, rownum, table):
        """ Получаем одну строку выбранной таблицы с номером rownum """
        with self.connection:
            return self.cursor.execute('SELECT * FROM {} WHERE id = ?'.format(table), (rownum,)).fetchone()

    def select_all_v2(self, table):
        """ Получаем все строки таблицы вне словаря """
        with self.connection:
            return self.cursor.execute('SELECT * FROM {} WHERE VOC = 0'.format(table)).fetchall()

    def select_single_category(self, cat):
        """ Получаем все строки с категорией cat """
        with self.connection:
            return self.cursor.execute('SELECT * FROM words WHERE CATEGORY = ?', (cat,)).fetchall()

    def select_cat_column(self):
        """ Получаем все категории"""
        with self.connection:
            z = []
            for i in range(self.count_rows('words')):
                z += self.cursor.execute('SELECT CATEGORY FROM words').fetchall()[i]
            return set(z)

    def count_rows(self, table):
        """ Считаем количество строк в выбранной таблице"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM {}'.format(table)).fetchall()
            return len(result)

    def get_vocabulary(self, table):
        """ Получаем все строки, занесенные в словарь в выбранной табблице """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM {0} WHERE VOC = 1'.format(table)).fetchall()
            return result

    def select_word_column(self):
        """ Получаем все cлова из словаря"""
        with self.connection:
            z = []
            for i in range(len(self.get_vocabulary('words'))):
                z += self.cursor.execute('SELECT WORD FROM words WHERE VOC = 1').fetchall()[i]
            return z

    def insertq(self, a, table):
        """ Ставим метку словаря"""
        with self.connection:
            sql = """
            UPDATE {} 
            SET VOC = '%s'
            WHERE ID = '%s'
            """.format(table) % (1, a)
            self.cursor.execute(sql)

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()