import psycopg2 as pg
from psycopg2 import Error
import psycopg2.extras
import csv

"""
DATABASE INFORMATION


SERVER: ec2-3-228-134-188.compute-1.amazonaws.com
DATABASE: dd5hvt80750lfu
PORT: 5432
USERNAME: fysyfysyrxbtwb
PASSWORD: c003474f786bc37b03b31d4f0377713a3a29becb8c9b111062db7ba496aa34e1

"""

"""
    DATABASE CONNECTION CLASS
"""
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

            ### DELETE THIS BEFORE SUBMISSION
            #self.hardResetDB()
            ###

            self.db_conn.commit()
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def disconnect_db(self):
        try:
            self.db_conn.close()
            print("disconnected")
        except pg.Error:
            print("error disconnecting")

    def hardResetDB(self) -> bool:
        try:
            cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            print(cur.execute(
                """
                    DROP TABLE IF EXISTS timeSeriesConfirmed CASCADE;
                    DROP SCHEMA IF EXISTS covidCases CASCADE;
                    CREATE SCHEMA covidCases;
                    SET SEARCH_PATH TO covidCases;
                    CREATE TABLE IF NOT EXISTS timeSeriesConfirmed (
                        combined TEXT NOT NULL,
                        PRIMARY KEY (combined)
                    );
                """
            ))
            print(cur.statusmessage) #DELETE AT END
            countries = getListOfCountries()
            for country in countries:
                cur.execute(
                    """
                        SET SEARCH_PATH TO covidCases;
                        INSERT INTO timeSeriesConfirmed(combined)
                        VALUES (' """ + country + """ ');
                                """)
                print(cur.statusmessage) #DELETE AT END
            cur.close()
        except pg.Error:
            print(cur.statusmessage)
            return False

    def insertNewData(self, data) -> bool:
        try:
            cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            for dataPoint in data:

                #Create Combined Key
                print(dataPoint)
                if isinstance(dataPoint['Province/State'],str):
                    combined = str(dataPoint.pop('Province/State')) + str(dataPoint.pop('Country/Region'))
                else:
                    dataPoint.pop('Province/State')
                    combined = dataPoint.pop('Country/Region')
                combined = ''.join(c for c in combined if c.isalnum())

                #Get rid of extra infom
                dataPoint.pop('Lat')
                dataPoint.pop('Long')

                print(dataPoint)



                for date in dataPoint:
                    cur.execute(
                        """
                        SET SEARCH_PATH TO covidCases;
                        ALTER TABLE timeseriesconfirmed
                            ADD COLUMN IF NOT EXISTS " """+ date +""" " INTEGER;
                        """
                    )

                    print("""
                        UPDATE timeseriesconfirmed
                            SET " """+ date +""" " = """+ str(dataPoint[date]) +"""
                            WHERE combined = ' """+ combined +""" ';
                        
                        """)

                    cur.execute(
                        """
                        UPDATE timeseriesconfirmed
                            SET " """+ date +""" " = """+ str(dataPoint[date]) +"""
                            WHERE combined = ' """+ combined +""" ';
                        
                        """
                    )
                    print(cur.statusmessage)

            cur.close()
            self.db_conn.commit()
            return True
        except pg.Error:
            print(cur.statusmessage)
            return False

    def viewAllData(self):
        pass

"""
    REQUEST FUNCTIONS
"""
def addCSV(data):
    covid = getConnection()
    covid.insertNewData(data)
    covid.disconnect_db()

def newCSV(data):
    covid = getConnection()
    print("DB has restarted", covid.hardResetDB())
    # covid.insertNewData(data)
    covid.disconnect_db()


def viewData():
    covid = getConnection()
    print(covid.viewAllData())
    covid.disconnect_db()


def deleteAllData():
    covid = getConnection()
    print(covid.hardResetDB())
    covid.disconnect_db()

"""
    HELPER FUNCTIONS
"""
def getConnection():
    covid = dbConnection()
    covid.startConnection("fysyfysyrxbtwb", "c003474f786bc37b03b31d4f0377713a3a29becb8c9b111062db7ba496aa34e1",
                          "ec2-3-228-134-188.compute-1.amazonaws.com", "5432", "dd5hvt80750lfu")
    return covid


def getListOfCountries():
    import os
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../csvExamples/time_series_covid19_confirmed_global.csv')


    countries = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            combined = row[0] + row[1]
            combined = ''.join(c for c in combined if c.isalnum())
            countries.append(combined)
    return countries