from connect_to_db import connect
import json

database = connect()
cursor = database.cursor()

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
