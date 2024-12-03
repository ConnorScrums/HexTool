import os
import pymysql
from dotenv import load_dotenv


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

    def getUserId(self, username, token):
        """
        Get the Users Id from the database (Primary Key)
        """
        if self.checkValidSession(username, token):
            load_dotenv()
            connection, cursor = self.connectToDatabase()
            sql = "SELECT idusers FROM users WHERE username = %s"
            cursor.execute(sql, username)
            connection.commit()
            results = cursor.fetchall()
            if results:
                connection.close()
                cursor.close()
                return results[0][0]

            connection.close()
            cursor.close()
            return False
        return False

    def addHash(self, hash_result, file_name, hash_method, check_sum, username, token):
        """
        Add the hash data to the database for a user if they are logged in
        """
        if self.checkValidSession(username, token):
            connection, cursor = self.connectToDatabase()
            userId = self.getUserId(username, token)
            sql = "SELECT * FROM hashes WHERE user_id = %s AND file_name = %s AND hash_method = %s"
            record = (userId, file_name, hash_method)
            cursor.execute(sql, record)
            connection.commit()
            hashExists = cursor.fetchall()
        
            if not hashExists:
              sql = "INSERT INTO hashes (user_id, hash_result, file_name, hash_method, check_sum) VALUES (%s, %s, %s, %s, %s);"
              record = (userId, hash_result, file_name, hash_method, check_sum)
              cursor.execute(sql, record)
              connection.commit()
            
            connection.close()
            cursor.close()

    def deleteHash(self, username, token, fileId):
        """
        Delete hash from the database for a user if they are logged in
        """
        if self.checkValidSession(username, token):
            connection, cursor = self.connectToDatabase()
            id = self.getUserId(username, token)
            print(fileId)
            sql = "DELETE FROM hashes WHERE file_id = %s;"
            record = (fileId)
            cursor.execute(sql, record)
            connection.commit()
            connection.close()
            cursor.close()

    def getUserHashes(self, username, token):
        """
        Get all hashes from the database for a user if they are logged in
        """
        if self.checkValidSession(username, token):
            id = self.getUserId(username, token)
            connection, cursor = self.connectToDatabase()
            sql = "SELECT * FROM hashes WHERE user_id = %s;"
            cursor.execute(sql, id)
            connection.commit()
            results = cursor.fetchall()
            if results:
                connection.close()
                cursor.close()
                return results

            connection.close()
            cursor.close()
            return False
        return False

    def setSessionToken(self, email, sessionToken):
        """
        Sets the session token in the DB for a new session
        """
        connection, cursor = self.connectToDatabase()
        query = "UPDATE users SET session_token = %s WHERE username = %s"
        cursor.execute(query, (sessionToken, email))
        connection.commit()
        results = cursor.fetchall()
        if results:
            connection.close()
            cursor.close()
            return True

        connection.close()
        cursor.close()
        return False

    def deleteSessionToken(self, username):
        """
        Delete the session token for current user after signout
        """
        connection, cursor = self.connectToDatabase()
        sql = "UPDATE users SET session_token = NULL = NULL WHERE username = %s"
        cursor.execute(sql, username)
        connection.commit()
        connection.close()

    def checkValidSession(self, username, token):
        """
        Check if the session is valid
        """
        connection, cursor = self.connectToDatabase()
        sql = "SELECT * FROM users WHERE username = %s AND session_token = %s;"
        cursor.execute(sql, (username, token))
        connection.commit()
        results = cursor.fetchall()
        if results:
            connection.close()
            cursor.close()
            return True

        connection.close()
        cursor.close()
        return False
