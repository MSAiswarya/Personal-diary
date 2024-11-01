import mysql.connector
try:
    mydb=mysql.connector.connect(host="localhost",user="root",password="aish@2001")
    mycursor=mydb.cursor()
    mycursor.execute("create database personal_diary")
except mysql.connector.Error as err:
    print("Something went wrong :""{}".format(err))