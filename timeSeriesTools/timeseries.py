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

            self.db_conn.commit()
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def disconnect_db(self):
        try:
            self.db_conn.close()
            print("disconnected")
        except pg.Error:
            print("error disconnecting")

    def hardResetTable(self,datatype) -> bool:
        try:
            cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            exe_string = """
                    SET SEARCH_PATH TO covidCases;
                    DROP TABLE IF EXISTS """ + getTableName(datatype) + """ CASCADE;
                    CREATE TABLE IF NOT EXISTS """ + getTableName(datatype) + """ (
                        combined TEXT NOT NULL,
                        PRIMARY KEY (combined)
                    );
                """
            print(exe_string)
            cur.execute(exe_string)
            cur.close()
            cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            countries = getListOfCountries()
            for country in countries:

                exe_string = """
                        INSERT INTO """ + getTableName(datatype) + """(combined)
                        VALUES (' """ + country + """ ');
                        """
                cur.execute(exe_string)
            cur.close()
        except pg.Error:
            print(cur.statusmessage)
            return False

    def insertData(self, data, datatype) -> bool:
        try:
            cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            # For each line in the csv file (each country)
            for count, dataPoint in enumerate(data):

                # Create Combined Key
                if isinstance(dataPoint['Province/State'], str):
                    combined = str(dataPoint.pop('Province/State')) + str(dataPoint.pop('Country/Region'))
                else:
                    dataPoint.pop('Province/State')
                    combined = dataPoint.pop('Country/Region')
                combined = ''.join(c for c in combined if c.isalnum())

                # Get rid of extra information
                dataPoint.pop('Lat')
                dataPoint.pop('Long')

                if count == 0:
                    for date in dataPoint:
                        exe_string = """
                            SET SEARCH_PATH TO covidCases;
                            ALTER TABLE """ + getTableName(datatype) + """
                                ADD COLUMN IF NOT EXISTS " """ + date + """ " INTEGER;
                            """
                        cur.execute(exe_string)

                # For each date/confirmed associated with that country
                for date in dataPoint:
                    exe_string = """
                        UPDATE """ + getTableName(datatype) + """
                            SET " """ + date + """ " = """ + str(dataPoint[date]) + """
                            WHERE combined = ' """ + combined + """ ';

                        """
                    cur.execute(exe_string)

            cur.close()
            self.db_conn.commit()
            return True
        except pg.Error:
            print(cur.statusmessage)
            return False

    def query_confirmed(self, date, combined, datatype):
        try:
            cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            print("here")
            if date == None and combined == None:  # Neither time nor country exists
                exe_string = """
                    SET SEARCH_PATH TO covidCases;
                    SELECT * from """ + getTableName(datatype) + """;
                    """
                print(exe_string)
                cur.execute(exe_string)
            elif date != None and combined == None:  # Time exists
                exe_string = """
                    SET SEARCH_PATH TO covidCases;
                    SELECT combined, " """ + date + """ " from """ + getTableName(datatype) + """;
                    """
                cur.execute(exe_string)
            elif date == None and combined != None:  # Country exists
                exe_string = """
                    SET SEARCH_PATH TO covidCases;
                    SELECT * from """ + getTableName(datatype) + """ where combined = ' """ + combined + """ ' ;
                    """
                cur.execute(exe_string)
            else:  # Both time and country exist
                exe_string = """
                    SET SEARCH_PATH TO covidCases;
                    SELECT combined, " """ + date + """ " from """ + getTableName(
                    datatype) + """ where combined = ' """ + combined + """ ' ;
                    """
                cur.execute(exe_string)
            return cur.fetchall()


        except pg.Error:
            print(cur.statusmessage)
            return False

    def viewAllData(self, datatype):
        try:
            cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            exe_string = """
                    SET SEARCH_PATH TO covidCases;
                    select * from """ + getTableName(datatype) + """;

                    """
            cur.execute(exe_string)
            data = cur.fetchall()
            cur.close()
            self.db_conn.commit()
            return data
        except pg.Error:
            print(cur.statusmessage)
            return False


"""
    REQUEST FUNCTIONS
"""

def addCSV(data, type: str):
    covid = getConnection()
    covid.insertData(data, type)
    covid.disconnect_db()

def newCSV(data, type: str):
    covid = getConnection()

    covid.hardResetTable(type)

    covid.insertData(data, type)
    covid.disconnect_db()

def viewData(type: str):
    covid = getConnection()
    data = covid.viewAllData(type)
    covid.disconnect_db()
    return data

def deleteAllData(type: str):
    covid = getConnection()

    covid.hardResetTable(type)

    covid.disconnect_db()

def query(date: str, combined: str, type: str):
    covid = getConnection()
    result = "ERROR INCORRECT QUERY"
    print("Type:", type, "Date:", date)
    result = covid.query_confirmed(date, combined, type)

    covid.disconnect_db()
    return result

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

def getTableName(type: str) -> str:
    if type == "confirmed":
        return "timeseriesconfirmed"
    if type == "deaths":
        return "timeseriesdeaths"
    if type == "recovered":
        return "timeseriesrecovered"