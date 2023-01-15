import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="database"
)

mycursor = mydb.cursor()

sql = "CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))"
mycursor.execute(sql)

sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"

data = [("John", "Highway 21"), ("Mario", "Lighway 45"), ("Tron", "Dark 13")]
for val in data :
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
