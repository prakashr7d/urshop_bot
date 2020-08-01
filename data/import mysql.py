import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="prakash",
  password="",
  database="urshop"
)

mycursor = mydb.cursor()


print(mycursor.execute("select pincode from clients"))
