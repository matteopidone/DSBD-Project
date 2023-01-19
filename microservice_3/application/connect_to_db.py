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

def execute(query):
    database = connect()
    cursor = database.cursor()
    data = False
    try:
        cursor.execute(query)
        data = cursor
    except Error as e:
        print("Error while execute the query", e)
    print(data)
    return data

def close(database):
    database.close()


# Close connection to Database