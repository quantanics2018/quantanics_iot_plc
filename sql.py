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

        sql = 'CREATE TABLE IF NOT EXISTS DataLog(Current int, Voltage int,'
        
        for i in range(0,14):
            sql += 'Relay' + str(i) + ' int,'

        sql += 'time timestamp default current_timestamp)'
        self.cur.execute(sql)
        self.db.commit()

    def push(self, current, voltage, relay_values):

        sql = "INSERT INTO DataLog(Current, Voltage,"
        
        for i in range(0,14):
            sql += 'Relay' + str(i) + ', '

        sql = sql[:-2] + ') '    
        sql += " VALUES("
        sql += str(current) + ','
        sql += str(voltage) + ','

        sql += ', '.join(relay_values)
        sql += ');'
        self.cur.execute(sql)
        self.db.commit()

        