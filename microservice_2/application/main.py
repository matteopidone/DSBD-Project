import mysql.connector

#https://www.w3schools.com/python/python_mysql_getstarted.asp

print("Start")
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="database"
)

print(mydb)

mycursor = mydb.cursor()

sql = "SELECT * FROM customers"
mycursor.execute(sql)

result = mycursor.fetchall()

for x in result:
    print(x)