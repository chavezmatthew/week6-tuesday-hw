import mysql.connector
from mysql.connector import Error

db_name = 'workout'
user = 'root'
password = 'Blackberry1!'
host = 'localhost'

def connection ():
    try:
        conn = mysql.connector.connect(
            database = db_name,
            user = user,
            password = password,
            host = host
        )

        if conn.is_connected():
            print("Successfully connected to the database!")
            return conn
    except Error as e:
        print (f"Error: {e}")
        return None