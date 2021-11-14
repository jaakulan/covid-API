import requests
from flask.wrappers import Response
import unittest
from app import app



URL = 'https://covidjaakalex.ue.r.appspot.com/daily'
SHRUNK_URL = 'https://covidjaakalex.ue.r.appspot.com/'


"""
URL = 'http://127.0.0.1:5000/daily'
SHRUNK_URL = 'http://127.0.0.1:5000'
"""

q_setup = False


class FlaskTest(unittest.TestCase):
    q_setup = False

    # check for response 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    # check if content return is text/html; charset=utf-8
    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.content_type, "text/html; charset=utf-8")
    
    # check if data returned for base
    def test_index_data(self):
        tester = app.test_client(self)
        response = tester.get("/")
        correctText = "Welcome to Jaakulan and Alexandra's Covid Api!"
        self.assertEqual(b"Welcome to Jaakulan and Alexandra's Covid Api!", response.data, "Should be "+ correctText)

    #test if data is posted correctly and can be viewed
    def test_post(self):
        files = {'file': open('./csvExamples/10-11-2021.test.csv','rb')}
        tester = app.test_client(self)
        response = tester.get("/deleteAll")
        response = requests.post(URL+'/addNewCSV', files=files)
        response = requests.get(URL+'/viewAll?type=json')
        files.get('file').close()
        print(response.text)
        correctText = '[{"region": null, "country": "Afghanistan", "combined": "Afghanistan", "deaths": 2201, "confirmed": 52513, "active": 0, "recovered": 41727, "to_char": "01-02-2021"}, {"region": null, "country": "Albania", "combined": "Albania", "deaths": 1181, "confirmed": 58316, "active": 23501, "recovered": 33634, "to_char": "01-02-2021"}, {"region": null, "country": "Algeria", "combined": "Algeria", "deaths": 2762, "confirmed": 99897, "active": 29740, "recovered": 67395, "to_char": "01-02-2021"}, {"region": null, "country": "Andorra", "combined": "Andorra", "deaths": 84, "confirmed": 8117, "active": 570, "recovered": 7463, "to_char": "01-02-2021"}]'
        self.assertEqual(correctText, response.text, "Should be "+ correctText)

    # check if data returned for base
    def test_deleteAll(self):
        files = {'file': open('./csvExamples/10-11-2021.test.csv','rb')}
        tester = app.test_client(self)
        response = tester.delete("/daily/deleteAll")
        response = requests.post(URL+'/addNewCSV', files=files)
        response = requests.delete(URL+'/deleteAll')
        response = requests.get(URL+'/viewAll?type=json')
        files.get('file').close()
        correctText = '[]'
        self.assertEqual(correctText, response.text, "Should be "+ correctText)

    # delete the whole database
    def test_deleteDatabase(self):
        files = {'file': open('./csvExamples/10-11-2021.test.csv','rb')}
        tester = app.test_client(self)
        response = tester.delete("/daily/deleteAll")
        response = requests.post(URL+'/addNewCSV', files=files)
        response = tester.delete("/deleteDB")
        response = requests.get(URL+'/viewAll?type=json')
        files.get('file').close()
        correctText = '[]'
        self.assertEqual(correctText, response.text, "Should be "+ correctText)

    # delete the whole database
    def test_deleteInfo(self):
        files = {'file': open('./csvExamples/10-11-2021.test.csv','rb')}
        tester = app.test_client(self)
        response = tester.delete("/daily/deleteAll")
        response = requests.post(URL+'/addNewCSV', files=files)
        response = tester.delete("/daily/deleteAll")
        response = requests.get(URL+'/viewAll?type=json')
        files.get('file').close()
        correctText = '[]'
        self.assertEqual(correctText, response.text, "Should be "+ correctText)

    # update existing database
    def test_update(self):
        tester = app.test_client(self)
        response = tester.get("/deleteAll")
        #add data
        files = {'file': open('./csvExamples/10-11-2021.test.csv','rb')}
        response = requests.post(URL+'/addNewCSV', files=files)
        files.get('file').close()
        #update with extra data
        files = {'file': open('./csvExamples/10-12-2021.test.csv','rb')}
        response = requests.patch(URL+'/updateWithCSV', files=files)
        files.get('file').close()
        #update existing data with new data
        files = {'file': open('./csvExamples/10-11-2021.update.test.csv','rb')}
        response = requests.patch(URL+'/updateWithCSV', files=files)
        files.get('file').close()
        response = requests.get(URL+'/viewAll?type=json')
        #find if update was successfull    
        correctText = '[{"region": "Tasmania", "country": "Australia", "combined": "Tasmania, Australia", "deaths": 0, "confirmed": 0, "active": 0, "recovered": 1, "to_char": "01-02-2021"}, {"region": "Victoria", "country": "Australia", "combined": "Victoria, Australia", "deaths": 0, "confirmed": 0, "active": 20, "recovered": 30, "to_char": "01-02-2021"}, {"region": null, "country": "Afghanistan", "combined": "Afghanistan", "deaths": 2, "confirmed": 5, "active": 0, "recovered": 41, "to_char": "01-03-2021"}, {"region": null, "country": "Albania", "combined": "Albania", "deaths": 1181, "confirmed": 58316, "active": 201, "recovered": 334, "to_char": "01-03-2021"}, {"region": null, "country": "Algeria", "combined": "Algeria", "deaths": 2762, "confirmed": 99897, "active": 0, "recovered": 395, "to_char": "01-03-2021"}, {"region": null, "country": "Afghanistan", "combined": "Afghanistan", "deaths": 0, "confirmed": 0, "active": 0, "recovered": 0, "to_char": "01-07-2021"}, {"region": null, "country": "Albania", "combined": "Albania", "deaths": 1, "confirmed": 6, "active": 1, "recovered": 4, "to_char": "01-07-2021"}, {"region": null, "country": "Algeria", "combined": "Algeria", "deaths": 2, "confirmed": 7, "active": 40, "recovered": 5, "to_char": "01-07-2021"}, {"region": null, "country": "Andorra", "combined": "Andorra", "deaths": 4, "confirmed": 7, "active": 0, "recovered": 73, "to_char": "01-07-2021"}]'
        self.assertEqual(correctText, response.text, "Should be "+ correctText)

    #query with only type
    def test_queries_one_type(self):
        # Ensure files are set up, if not already
        global q_setup
        if q_setup == False:
            setup_queries(self)
            q_setup = True

        
        response = requests.get(URL + '/info?type=json')
        print(response.text)
        correctText = "Must Specify at least one data query!"
        self.assertEqual(correctText, response.text, "For query with only type, Should be "+ correctText)

    # query with one type, one data
    def test_queries_one_type_one_data(self):
        # Ensure files are set up, if not already
        global q_setup
        if q_setup == False:
            setup_queries(self)
            q_setup = True

        response = requests.get(URL + '/info?type=json&data=deaths')
        correctText = '[{"deaths": 2201}, {"deaths": 1181}, {"deaths": 2762}, {"deaths": 84}, {"deaths": 0}, {"deaths": 0}, {"deaths": 2}, {"deaths": 1181}, {"deaths": 2762}]'
        self.assertEqual(correctText, response.text, "For query with one type, one data, Should be "+ correctText)

    # query with one type, one data, one specific date
    def test_queries_one_type_one_data_one_date(self):
        #Ensure files are set up, if not already
        global q_setup
        if q_setup == False:
            setup_queries(self)
            q_setup = True

        response = requests.get(URL + '/info?type=json&data=deaths&date=10-11-2021')
        correctText = '[{"deaths": 2201}, {"deaths": 1181}, {"deaths": 2762}, {"deaths": 84}]'
        self.assertEqual(correctText, response.text, "For query with one type, one data, one specific date, Should be "+ correctText)

    # query with one type, one data, one range of dates
    def test_queries_one_type_one_data_range_date(self):
        # Ensure files are set up, if not already
        global q_setup
        if q_setup == False:
            setup_queries(self)
            q_setup = True

        response = requests.get(URL + '/info?type=json&data=deaths&dateStart=10-12-2021&dateEnd=10-15-2021')
        correctText = '[{"deaths": 2}, {"deaths": 1181}, {"deaths": 2762}, {"deaths": 0}, {"deaths": 0}]'
        self.assertEqual(correctText, response.text, "For query with one type, one data, one range of dates, Should be "+ correctText)

    # query with one type, one data, one range of dates and country
    def test_queries_one_type_one_data_range_date_range_country(self):
        # Ensure files are set up, if not already
        global q_setup
        if q_setup == False:
            setup_queries(self)
            q_setup = True

        response = requests.get(URL + '/info?type=json&data=deaths&dateStart=10-12-2021&dateEnd=10-15-2021&country=Australia')
        correctText = '[{"deaths": 0}, {"deaths": 0}]'
        self.assertEqual(correctText, response.text, "For query with one type, one data, one range of dates and country, Should be "+ correctText)

    # query with wrong type
    def test_queries_wrong_type(self):
        # Ensure files are set up, if not already
        global q_setup
        if q_setup == False:
            setup_queries(self)
            q_setup = True

        response = requests.get(URL + '/info?type=XML&data=deaths')
        correctText = 'Return type was not valid Or type was not specified'
        self.assertEqual(correctText, response.text, "For query with wrong type, Should be "+ correctText)

    # query with wrong date
    def test_queries_wrong_date(self):
        # Ensure files are set up, if not already
        global q_setup
        if q_setup == False:
            setup_queries(self)
            q_setup = True

        print(URL +'/info?type=json&date=12121&data=deaths' )
        response = requests.get(URL + '/info?type=json&date=12121&data=deaths')
        correctText = '12121 is an incorrect data format, should be MM-DD-YYYY'
        self.assertEqual(correctText, response.text, "For query with wrong date, Should be "+ correctText)

    # query with combined_key that doesnt exist
    def test_queries_wrong_country(self):
        # Ensure files are set up, if not already
        global q_setup
        if q_setup == False:
            setup_queries(self)
            q_setup = True

        response = requests.get(URL + '/info?type=json&combined=congobongodongo&data=deaths')
        correctText = '[]'
        self.assertEqual(correctText, response.text, "For query with combined_key that doesnt exist, Should be "+ correctText)

def setup_queries(tester):
    tester = app.test_client(tester)
    response = tester.get("/deleteAll")
    #add data
    files = {'file': open('./csvExamples/10-11-2021.test.csv','rb')}
    response = requests.post(URL+'/addNewCSV', files=files)
    files.get('file').close()
    #update with extra data
    files = {'file': open('./csvExamples/10-12-2021.test.csv','rb')}
    response = requests.patch(URL+'/updateWithCSV', files=files)
    files.get('file').close()

    
if __name__ == "__main__":
    unittest.main()

