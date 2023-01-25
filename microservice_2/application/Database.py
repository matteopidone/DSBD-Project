from time import sleep
import mysql.connector
import os

class DataStorageDatabaseClass():
    def connect(self):
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

    def insert_or_update_stats(self) :
        return True
    
    def insert_or_update_prediction(self) :
        return True

    def insert_or_update_metadata(self) :
        return True

# Close connection to Database