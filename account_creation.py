"""
AccountCreation, connect to DB and create a
new user account with input from the
account_creation webpage
"""
import pymysql

class AccountCreation():
    """Handle account creation"""

    def connect_to_database(self):
        """
        Connect to the DB, returns the connection & cursor
        """
        connection = pymysql.connect(host = 'agileteam2db.c922gmyakzhj.us-east-1.rds.amazonaws.com',
                                    user = 'admin',password = 'Team2dbpw1!', database = 'HashingApp')
        connection_cursor = connection.cursor()
        return connection,connection_cursor


    def create_account(self, email, password):
        """
        Takes input from webpage and inserts into users table in DB
        """
        con,cursor = self.connect_to_database()

        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(sql, (email, password))
        con.commit()

        con.close
