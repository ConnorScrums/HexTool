import os
import pymysql
from dotenv import load_dotenv
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

    def getUserId(self):
        """
        Get the Users Id from the database (Primary Key)
        """
        load_dotenv()
        connection, cursor = self.connectToDatabase()
        sql = "SELECT idusers FROM users WHERE username = %s"
        cursor.execute(sql, current_app.config["USERNAME"])
        results = cursor.fetchall()
        if results:
            connection.close()
            return results[0][0]

        connection.close()
        return False

    def addHash(self, hash_result, file_name, hash_method, check_sum):
        """
        Add the hash data to the database for a user if they are logged in
        """
        if current_app.config["USERNAME"] != "":
            connection, cursor = self.connectToDatabase()
            userId = self.getUserId()
            print("USER ID:")
            print(userId)
            sql = "INSERT INTO hashes (user_id, hash_result, file_name, hash_method, check_sum) VALUES (%s, %s, %s, %s, %s);"
            record = (userId, hash_result, file_name, hash_method, check_sum)
            cursor.execute(sql, record)
            connection.commit()
            connection.close()

    def deleteHashes(self):
        """
        Delete all hashes from the database for a user if they are logged in
        """
        if current_app.config["USERNAME"] != "":
            connection, cursor = self.connectToDatabase()
            id = self.getUserId()
            sql = "DELETE FROM hashes WHERE user_id = %s;"
            cursor.execute(sql, id)
            connection.commit()
            connection.close()

    def getUserHashes(self):
        """
        Get all hashes from the database for a user if they are logged in
        """
        id = self.getUserId()
        connection, cursor = self.connectToDatabase()
        sql = "SELECT * FROM hashes WHERE user_id = %s;"
        cursor.execute(sql, id)
        results = cursor.fetchall()
        if results:
            connection.close()
            return results

        connection.close()
        return False
