from typing import List, Optional
import psycopg2 as pg
from psycopg2 import Error
import psycopg2.extras


class dbConnection:
    def __init__(self) -> None:
        """Initialize this Recommender, with no database connection yet.
        """
        self.db_conn = None

    def startConnection(self, user: str, password: str, host: str, port: str, database: str):
        try:
            # Connect to an existing database
            self.db_conn = pg.connect(user=user,
                                        password=password,
                                        host=host,
                                        port=port,
                                        database=database)
            print("you are connected to database")
            cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(
                """
                    CREATE SCHEMA IF NOT EXISTS covidCases;
                    CREATE TABLE IF NOT EXISTS dailyCases (
                        combined TEXT NOT NULL,
                        deaths INT NOT NULL,
                        confirmed INT NOT NULL,
                        active INT NOT NULL,
                        recovered INT NOT NULL,
                        d TIMESTAMP NOT NULL,
                        PRIMARY KEY (combined)
                    );
                """
                )
            cur.close()
            self.db_conn.commit()
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def disconnect_db(self):
        try:
            self.db_conn.close()
            print("disconnected")
        except pg.Error:
            print("error disconnecting")

    def restartDB(self) -> bool:
        try:
            cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(
                """
                    SET SEARCH_PATH TO covidCases;
                    DROP TABLE IF EXISTS dailyCases CASCADE;    
                    CREATE TABLE dailyCases (
                        combined TEXT NOT NULL,
                        deaths INT NOT NULL,
                        confirmed INT NOT NULL,
                        active INT NOT NULL,
                        recovered INT NOT NULL,
                        d TIMESTAMP NOT NULL,
                        PRIMARY KEY (combined)
                    );
                """
                )
            self.db_conn.commit()
            cur.close()
            return True
        except pg.Error:
            print(cur.statusmessage)
            return False
    
    def insertNewData(self, data)->bool:
        try:
            cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            for dataPoint in data:
                cur.execute(
                    """
                    Insert into dailyCases VALUES
                    (%s, %s, %s, %s, %s, %s);
                    
                    """,
                    (dataPoint['Combined_Key'], dataPoint['Deaths'], dataPoint['Confirmed'], dataPoint['Active'], dataPoint['Recovered'], dataPoint['Last_Update'])
                    )
                print(cur.statusmessage)
            self.db_conn.commit()
            cur.close()
            return True
        except pg.Error:
            print(cur.statusmessage)
            return False
    
    def viewAllData(self):
        try:
            cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(
                    """
                    select * from dailyCases
                    
                    """
                    )
            cur.statusmessage
            data = cur.fetchall()
            cur.close()
            self.db_conn.commit()
            return data
        except pg.Error:
            print(cur.statusmessage)
            return False
        
    def queryByComKey(self, query):

        return

        
def getConnection():
    covid = dbConnection()
    covid.startConnection("fysyfysyrxbtwb", "c003474f786bc37b03b31d4f0377713a3a29becb8c9b111062db7ba496aa34e1", "ec2-3-228-134-188.compute-1.amazonaws.com", "5432", "dd5hvt80750lfu")
    return covid

def newCSV(data):
    covid = getConnection()
    print("DB has restarted", covid.restartDB())
    covid.insertNewData(data)
    covid.disconnect_db()
        
def viewData(data):
    covid = getConnection()
    data = covid.viewAllData()
    covid.disconnect_db()
    return data

def deleteAllData():
    covid = getConnection()
    print(covid.restartDB())
    covid.disconnect_db()

