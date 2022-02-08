import mysql.connector
from setuptools import Require
from dotenv import load_dotenv, find_dotenv
import os




def connect_sql():

    load_dotenv(find_dotenv())

    host = os.environ.get('HOST')                   #nämä saadaan .env tiedostosta
    user = os.environ.get('SQL_USER')
    password = os.environ.get('PASSWORD')

    mydb = mysql.connector.connect(
        host= host,
        user= user,
        password = password,
    )
    return(mydb)


mydb = connect_sql()     #yhteys tietokantaan

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

for x in mycursor:
  print(x)


