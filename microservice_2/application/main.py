import mysql.connector

print("Start")
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password"
)

print(mydb)