import os
import pymysql
from dotenv import load_dotenv
from .database_password_helper import DatabasePasswordHelper
from flask import current_app

class DatabaseUtility:
    """Handle database querys"""

    def connectToDatabase(self):
       """
       Connect to the DB, returns the connection & cursor
       """
       connection = pymysql.connect(
           host=os.getenv("DB_ENDPOINT"),
           user=os.getenv("DB_USERNAME"),
           password=os.getenv("DB_PASSWORD"),
           database=os.getenv("DB_NAME"),
       )
       connection_cursor = connection.cursor()
       return connection, connection_cursor
       #TODO MAYBE NEED TO CLOSE DATABASE CONNECTION CHECK THIS
    
    def getUserId(self):
        load_dotenv()
        connection, cursor = self.connectToDatabase()
        sql = "SELECT idusers FROM users WHERE username = %s"
        cursor.execute(sql, current_app.config["USERNAME"])
        results = cursor.fetchall()
        if results:
            print(results[0][0])
            return results[0][0]
        
        return False

    def addHash(self, hash_result, file_name, hash_method, check_sum):
        if current_app.config["USERNAME"] != "":
            connection, cursor = self.connectToDatabase()
            userId = self.getUserId()
            print("USER ID:")
            print(userId)
            sql = "INSERT INTO hashs (user_id, hash_result, file_name, hash_method, check_sum) VALUES (%s, %s, %s, %s, %s);"
            record = (userId, hash_result, file_name, hash_method, check_sum)
            cursor.execute(sql, record)
            connection.commit()

    def deleteHashs(self):
        if current_app.config["USERNAME"] != "":
            print("IN DELETE")
            connection,cursor = self.connectToDatabase()
            id = self.getUserId()
            sql = "DELETE FROM hashs WHERE user_id = %s;"
            cursor.execute(sql, id)
            connection.commit()
            print("DELETE ALL HASHS SUCCESSFUL")

    def getUserHashs(self):
        id = self.getUserId()
        connection, cursor = self.connectToDatabase()
        sql = "SELECT * FROM hashs WHERE user_id = %s;"
        cursor.execute(sql, id)
        results = cursor.fetchall()
        if results:
            print(results)
            return results
        
        return False

