# db_connector.py
import mysql.connector
from mysql.connector import Error

def connect():
    """Connect to MySQL Database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='price_scrapper',
            user='root',
            password=''
        )
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

def close(connection):
    """Close the connection to the database"""
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")
