import mysql.connector
import os

def connect():
    return mysql.connector.connect(
        host=os.environ['MYSQL_HOST'],
        user="root",
        password="password",
        database="database"
    )

database = connect()
cursor = database.cursor()

cursor.execute('SHOW TABLES')

for x in cursor:
    print(x)