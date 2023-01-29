from Database import DataStorageDatabaseClass
from multiprocessing import Process
from MessageConsumer import start_consumers 
from gRPCServer import serve
import json

""" Main Function """
def main():
    db_instance = DataStorageDatabaseClass()
    database = db_instance.connect()
    cursor = database.cursor()
    init_database(cursor)
    p = Process(target=start_consumers, args=[DataStorageDatabaseClass()])
    p.start()
    serve()

""" Function to Initialize the Database """
def init_database(cursor):

    try:
        file = open("../database_schema.json", "r")
    except FileNotFoundError:
        print("File not found.")

    data = json.load(file) 
    file.close()

    for table in data['tables']:
        query = "CREATE TABLE " + table['name'] + " ( "
        for column in table['columns']:
            query += column['name'] + " " + column['type'] + ", "
        query += table['primary_key']
        if table['foreign_key']:
            query += ", " + table['foreign_key']
        query += " );"
        cursor.execute(query)
        print("Table '" + table['name'] + "' created")

""" Start Main Script """

if __name__ == '__main__':
    main()