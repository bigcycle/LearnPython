# -*- coding:utf-8 -*-

import MySQLdb
from Tool import Tool


class MySQL:
    """docstring for ClassName"""
    def __init__(self):
        self.getTime = Tool().getCurrentTime
        self.printf = Tool().printf
        try:
            self.db = MySQLdb.connect('127.0.0.1', 'root', 'root', 'iask_db')
            self.cur = self.db.cursor()
        except MySQLdb.Error, e:
            self.printf("Error connecting database:",
                        e.args[0], e.args[1], "\n")

    def insertData(self, table, my_dict):
        try:
            self.db.set_character_set('utf8')
            cols = ', '.join(my_dict.keys())
            values = '", "'.join(my_dict.values())
            sql = "INSERT INTO %s (%s) VALUES (%s)" % (
                table,
                cols,
                '"' + values + '"')
            # print sql
            try:
                result = self.cur.execute(sql)
                insert_id = self.db.insert_id()
                self.db.commit()
                if result:
                    return insert_id
                else:
                    return 0
            except MySQLdb.Error, e:
                self.db.rollback()
                self.printf("Insert Data failed:", e.args[0], e.args[1], "\n")
                self.printf(sql + "\n")
        except MySQLdb.Error, e:
            self.printf("Database Error:", e.args[0], e.args[1], "\n")
