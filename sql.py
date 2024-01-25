import mysql.connector

class SQL():

    def __init__(self) -> None:
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="")
        self.default_initializaiton()
        
    def default_initializaiton(self):

        self.cur = self.db.cursor()

        sql = 'CREATE DATABASE IF NOT EXISTS TB'
        self.cur.execute(sql)
        self.db.commit()

        sql = 'USE TB'
        self.cur.execute(sql)
        self.db.commit()

        sql = 'CREATE TABLE IF NOT EXISTS DataLog(Current1 int, Current2 int, Voltage1 int, Voltage2 int,'
        
        for i in range(0,14):
            sql += 'Relay' + str(i) + ' int,'

        sql += 'time timestamp default current_timestamp)'
        self.cur.execute(sql)
        self.db.commit()

    def push(self, current1, current2, voltage1, voltage2, relay_values):

        sql = "INSERT INTO DataLog(Current1, Current2, Voltage1, Voltage2,"
        
        for i in range(0,14):
            sql += 'Relay' + str(i) + ', '

        sql = sql[:-2] + ') '    
        sql += " VALUES("
        sql += str(current1) + ','
        sql += str(current2) + ','
        sql += str(voltage1) + ','
        sql += str(voltage2) + ','

        sql += ', '.join(relay_values)
        sql += ');'
        self.cur.execute(sql)
        self.db.commit()

        