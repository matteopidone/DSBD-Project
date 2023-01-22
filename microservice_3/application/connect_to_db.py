from time import sleep
import mysql.connector
import os

def connect():
    while True:
        try:
            sleep(5)
            print('Trying to connect to MySQL Host...')
            database = mysql.connector.connect(
                host=os.environ['MYSQL_HOST'],
                user="root",
                password="password",
                database="database"
            )
            if database.is_connected():
                print('Connection established')
                break
        except:
            print('Error during connection : MySQL Host not available')
            print('Retry sooner...')

    return database

def close(database):
    database.close()


# Close connection to Database