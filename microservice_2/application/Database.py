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

    def insert_or_update_stats(self, metric_name, value) :
        db = self.connect()
        cursor = db.cursor()
        try :
            cursor.execute()
            query_result = cursor.fetchone()
            if query_result :
                return True
            else :
                return False
        except :
            print("Error while execute the query")
            return False
        finally:
            cursor.close()
            db.close()
    
    def insert_or_update_prediction(self, metric_name, value) :
        db = self.connect()
        cursor = db.cursor()
        try :
            cursor.execute()
            query_result = cursor.fetchone()
            if query_result :
                return True
            else :
                return False
        except :
            print("Error while execute the query")
            return False
            
        finally:
            cursor.close()
            db.close()

    def insert_or_update_metadata(self, metric_name, value) :
        db = self.connect()
        cursor = db.cursor()
        try :
            cursor.execute()
            query_result = cursor.fetchone()
            if query_result :
                return True
            else :
                return False
        except :
            print("Error while execute the query")
            return False
        finally:
            cursor.close()
            db.close()

# Close connection to Database