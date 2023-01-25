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
        
    def get_all_metrics(self) :
        db = self.connect()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM metriche")
            query_result = cursor.fetchall()
            if query_result :
                return str(query_result).strip('[]')
            else :
                return str()
        except :
            print("Error while execute the query")
            return str()
        finally:
            cursor.close()
            db.close()
    
    def get_metadata_for_metrics(self, id_metric) :
        db = self.connect()
        cursor = db.cursor()
        try :
            cursor.execute("Select nome, metadata FROM metriche WHERE id = %s LIMIT 1", (id_metric,))
            query_result = cursor.fetchone()
            if query_result :
                return  str(query_result).strip('[]')
            else :
                return str()
        except :
            print("Error while execute the query")
            return str()
        finally:
            cursor.close()
            db.close()
            
    def get_history_for_metrics(self, id_metric) :
        db = self.connect()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT metriche.nome, statistiche.nome, statistiche_metriche.1h, statistiche_metriche.3h, statistiche_metriche.12h FROM metriche JOIN statistiche_metriche ON metriche.id=statistiche_metriche.id_metrica JOIN statistiche on statistiche.id=statistiche_metriche.id_statistica WHERE metriche.id= %s", (id_metric,))
            query_result = cursor.fetchall()
            if query_result :
                return  str(query_result).strip('[]')
            else :
                return str()
        except :
            print("Error while execute the query")
            return str()
        finally:
            cursor.close()
            db.close()

# Close connection to Database