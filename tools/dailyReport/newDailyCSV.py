from typing import List, Optional
import psycopg2 as pg
from psycopg2 import Error
import psycopg2.extras


class dbConnection:
    def __init__(self) -> None:
        """Initialize this Recommender, with no database connection yet.
        """
        self.db = None

    def startConnection(user: str, password: str, host: str, port: str, database: str):
        try:
            # Connect to an existing database
            db = pg.connect(user="postgres",
                                        password="pynative@#29",
                                        host="127.0.0.1",
                                        port="5432",
                                        database="postgres_db")
            print("you are connected to database")
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
                    DROP SCHEMA IF EXISTS covidCases CASCADE;
                    CREATE SCHEMA covidCases;
                    SET SEARCH_PATH TO covidCases;
                    CREATE TABLE dailyCases (
                        combined TEXT NOT NULL,
                        deaths INT NOT NULL,
                        confirmed INT NOT NULL,
                        active INT NOT NULL,
                        recovered INT NOT NULL,
                        d TIMESTAMP NOT NULL
                        PRIMARY KEY (combined)
                    );
                """
                )
            cur.close()
            self.db_conn.commit()
            return True
        except pg.Error:
            print(cur.statusmessage)
            return False
    
    def insertData(self, data)->bool:
        try:
            cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(
                """
                    
                """
                )
            cur.close()
            self.db_conn.commit()
            return True
        except pg.Error:
            print(cur.statusmessage)
            return False

def newCSV(self, data):
    covid = dbConnection()
    covid.startConnection(user, password, host, port, database)
    covid.insert(data)
    covid.restartDB()
    covid.disconnect_db()
        