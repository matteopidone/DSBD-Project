from connect_to_db import connect
from time import sleep
import json
import consumer

""" Main Function """
def main():
    database = connect()
    cursor = database.cursor()
    init_database(cursor)

    while True:
        cursor.execute("SHOW TABLES")
        for x in cursor:
            print(x)
        print('Sleeping...')
        sleep(10)

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
