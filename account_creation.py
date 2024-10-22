import pymysql

class AccountCreation():
    def connectToDataBase(self): 
        connection = pymysql.connect(host = 'agileteam2db.c922gmyakzhj.us-east-1.rds.amazonaws.com', user = 'admin', 
                                     password = 'Team2dbpw1!', database = 'HashingApp')
        connectionCursor = connection.cursor()
        return connection,connectionCursor

    def createAccount(self, email, password):
        con,cursor = self.connectToDataBase()
        print(email, password)

        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(sql, (email, password))
        con.commit()

        con.close
        