from connect_to_db import connect
from time import sleep
import json
from multiprocessing import Process
from MessageConsumer import start_consumers 
from gRPCServer import serve

""" Main Function """
def main():
    database = connect()
    cursor = database.cursor()
    init_database(cursor)
    p = Process(target=start_consumers)
    p.start()
    serve()

""" Function to Initialize the Database """
def init_database(cursor):
    # try and catch da inserire
    file = open("../database_schema.json", "r")
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