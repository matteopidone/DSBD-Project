from connect_to_db import connect

database = connect()
cursor = database.cursor()

cursor.execute("SHOW TABLES")

for x in cursor:
    print(x)