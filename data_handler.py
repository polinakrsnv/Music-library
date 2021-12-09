# -*- coding: utf-8 -*-
import config
from hashlib import md5
import psycopg2

class SQLighter:
    def __init__(self, database_name='postgres'):
        #database_name = 'postgres'
        conn = psycopg2.connect(dbname=database_name, user='mlib_admin',
                                password='Password1', host='mlib.postgres.database.azure.com')
        self.connection = conn
        self.cursor = self.connection.cursor()

    def get_genre(self):
        with self.connection:
            self.cursor.execute("SELECT genre.name FROM genre")
            return self.cursor.fetchall()
