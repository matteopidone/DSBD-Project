from time import sleep
from mysql.connector import MySQLConnection, Error
import mysql.connector
import os
import ast

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
            time = value['time']
            for stats in value['stats'] :
                id_metric = 'SELECT id FROM metriche WHERE nome = "' + str(metric_name) + '"'
                id_statistics = 'SELECT id FROM statistiche WHERE nome = "' + str(stats['name']) + '"'
                query = 'INSERT INTO statistiche_metriche (id_metrica, id_statistica,' + str(time) + ') VALUES ((' + str(id_metric) + '), (' + id_statistics + '),' + str(stats['value']) +') ON DUPLICATE KEY UPDATE ' + str(time) + ' = '+ str(stats['value']) +';'
                
                cursor.execute(query)
                query_result = db.commit()
                if cursor.rowcount != 0 :
                    continue 
                else :
                    return False
            return True
        except Error as e :
            print("Error while execute the query ", e)
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
            id_metric = 'SELECT m2.id FROM metriche AS m2 WHERE m2.nome = "' + str(metric_name) + '"'
            query = 'INSERT INTO metriche (id, nome, metadata) VALUES ((' + str(id_metric) + '), "' + str(metric_name) +'", "' + str(value) + '") ON DUPLICATE KEY UPDATE metadata = "'+ str(value) + '";'
            cursor.execute(query)
            query_result = db.commit()
            if cursor.rowcount != 0 :
                print("METADATA UPDATED")
                return True 
            else :
                return False
        except Error as e :
            print("Error while execute the query ", e)
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
    
    def get_all_statistics(self) :
        db = self.connect()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM statistiche")
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

    def insert_or_update_stats_conf(self, stats_list) :
        db = self.connect()
        cursor = db.cursor()
        stats_list_dict = ast.literal_eval(stats_list)
        try :            
            for stats in stats_list_dict :
                cursor.execute('INSERT INTO statistiche (nome) VALUES (%s)', (str(stats),))
                query_result = db.commit()
                if cursor.rowcount != 0 :
                    print("Metric inserted")
                    continue 
                else :
                    print("Metric NOT inserted")
                    return str(False)
            return str(True)
        except Error as e :
            print("Error while execute the query ", e)
            return str(False)
        finally:
            cursor.close()
            db.close()

    def insert_or_update_metrics_conf(self, metric_list) :
        db = self.connect()
        cursor = db.cursor()
        metric_list_dict = ast.literal_eval(metric_list)
        print(metric_list_dict)
        try :            
            for metric in metric_list_dict :
                cursor.execute('INSERT INTO metriche (nome) VALUES (%s)', (str(metric),))
                query_result = db.commit()
                if cursor.rowcount != 0 :
                    print("Metric inserted")
                    continue 
                else :
                    print("Metric NOT inserted")
                    return str(False)
            return str(True)
        except Error as e :
            print("Error while execute the query ", e)
            return str(False)
        finally:
            cursor.close()
            db.close()

# Close connection to Database