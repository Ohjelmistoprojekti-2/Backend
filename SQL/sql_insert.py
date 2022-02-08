import mysql.connector
from sql_connector import connect_sql




def sql_insert(sql,values):
    '''
    sql muodossa  "INSERT INTO customers (name, address) VALUES (%s, %s)"
    values muodossa ("John", "Highway 21")
    '''



    mydb = connect_sql()  #haetaan yhteys tietokantaan
    mycursor = mydb.cursor()

    mycursor.execute(sql, values)

    mydb.commit()

    return print(mycursor.rowcount, "Tieto tallennettu")




