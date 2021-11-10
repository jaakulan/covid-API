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
                    SET SEARCH_PATH TO covidCases;
                    CREATE TABLE IF NOT EXISTS dailyCases (
                        region TEXT NOT NULL,
                        country TEXT NOT NULL,
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
                        region TEXT NOT NULL,
                        country TEXT NOT NULL,
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
                print(dataPoint['Province_State'], dataPoint['Country_Region'])
                cur.execute(
                    """
                    SET SEARCH_PATH TO covidCases;
                    Insert into dailyCases VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s);
                    
                    """,
                    (dataPoint['Province_State'], dataPoint['Country_Region'], dataPoint['Combined_Key'], dataPoint['Deaths'], dataPoint['Confirmed'], dataPoint['Active'], dataPoint['Recovered'], dataPoint['Last_Update'])
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
            combined = "d = d"
            cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(
                    """
                    SET SEARCH_PATH TO covidCases;
                    select * from dailyCases where """ +combined+ """ ;
                    
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
        
    def query(self, data, dates, countries, region, key):
        try:
            print(data, dates, countries, region, key)
            cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            cur.execute(
                    """
                    SET SEARCH_PATH TO covidCases;
                    select """ +data+ """ from dailyCases
                    where (""" +key+ """ Or
                    """ +countries+ """ Or
                    """ +region+ """) and
                    """ +dates+ """;
                    """
                    )
            print(cur.statusmessage)
            info = cur.fetchall()
            cur.close()
            self.db_conn.commit()
            print("the info is ")
            print(data, info)
            return info
        except pg.Error:
            print(cur.statusmessage)
            return False

        
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

def queryData(data, dates, countries, region, key):
    covid = getConnection()
    data = dataString(data[1])
    print(dates)
    dates = dateString(dates[1])
    countries = countryString(countries[1])
    region = regionString(region[1])
    key= keyString(key[1])
    data = covid.query(data, dates, countries, region, key)
    covid.disconnect_db()

#########################################################__helper functions__#######################################

def dataString(data):
    return ",".join(data)

def dateString(dates):
    #3 cases
    length = len(dates)
    print(dates)
    if(length==2):                                                           #case 1: two dates
        return "d >= '" +dates[0]+" 00:00:00'"+" AND d <= '"+dates[1]+" 23:59:59'"
    elif(length==1):                                                         #case 2: one date
        return "d >= '"+dates[0]+" 00:00:00'"+" AND d <= '"+dates[0]+" 23:59:59'"
    else:                                                                    #case 3: no dates
        return "d = d"

def countryString(countries):
    #if query has countries
    if(len(countries)>= 1):
        for i in range(len(countries)):
            countries[i] = "'"+countries[i]+"'"
        countryList = ",".join(countries)
        return "country in ("+countryList+")"
    #if query has no countries
    else:
        return "country = country"

def regionString(regions):
    #if query has regions
    if(len(regions)>= 1):
        for i in range(len(regions)):
            regions[i] = "'"+regions[i]+"'"
        regionList = ",".join(regions)
        return "region in ("+regionList+")"
    #if query has no regions
    else:
        return "region = region"

def keyString(keys):
    #if query has regions
    if(len(keys)>= 1):
        for i in range(len(keys)):
            keys[i] = "'"+keys[i]+"'"
        keyList = ",".join(keys)
        return "combined in ("+keyList+")"
    #if query has no regions
    else:
        return "combined = combined"

    