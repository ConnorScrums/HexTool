"""
AccountCreation, connect to DB and create a
new user account with input from the
account_creation webpage
"""

import os
import pymysql
from dotenv import load_dotenv
from .database_password_helper import DatabasePasswordHelper
from flask import current_app


class AccountCreation:
    """Handle account creation"""

    def connect_to_database(self):
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

    def create_account(self, email, password):
        """
        Takes input from webpage and inserts into users table in DB
        """
        load_dotenv()
        db_helper = DatabasePasswordHelper()
        con, cursor = self.connect_to_database()
        password = db_helper.hash_password(password)
        if not self.does_email_exist(email, cursor):
            sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(sql, (email, password))
            con.commit()
            con.close()
            return True

        con.close()
        return False

    def does_email_exist(self, email, cursor):
        """
        Checks if user with entered email is already in the DB
        """
        sql = "SELECT * FROM users WHERE username = %s"
        cursor.execute(sql, (email))
        results = cursor.fetchall()
        if results:
            return True

        return False

    def login(self, email, password):
        """
        Takes input from the webpage and attempts to validate the user in the database
        """
        load_dotenv()
        db_helper = DatabasePasswordHelper()
        connection, cursor = self.connect_to_database()
        password = db_helper.hash_password(password)

        if self.does_email_exist(email, cursor):
            sql = "SELECT password FROM users WHERE username = %s"
            cursor.execute(sql, (email))
            results = cursor.fetchall()

            if results[0][0] == password[:45]:
                current_app.config["USERNAME"] = email
                connection.close()
                return True
            else:
                connection.close()
                return False