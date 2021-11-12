from cleaningTools.dataCleaning import checkDates, dataQuery, infoValidity


try:
    import unittest
    from cleaningTools import dataCleaning as clean 
except Exception as e:
    print("Some Modules are Missing {} ".format(e))

class cleaningTest(unittest.TestCase):

    def test_infoValidity(self):
        falseValidity = clean.infoValidity([False,"black sheep"],[True],[False],[True],[False])
        trueValidity = clean.infoValidity([True],[True],[True],[True],[True])
        self.assertEqual([False,"black sheep"], falseValidity,"False Validity Error Should be" + '[False,"black sheep"]')
        self.assertEqual([True, []], trueValidity,"False Validity Error Should be" + '[True, []]' )

    def test_locationQuery(self):
        location = clean.locationQuery([])
        self.assertEqual(location, [True, []], "Should be true for an empty location query")
        location = clean.locationQuery(['hello_hi', "cuba"])
        self.assertEqual(location, [True, ["hello hi", "cuba"]], "Should be true with location queries formatted")

    def test_dateQuery(self):
        date = clean.dateQuery([],[],['10-10-2021'])
        rangeDates = clean.dateQuery(['10-13-2021'],['10-19-2021'],[])
        self.assertEqual(date, [True, ['10-10-2021']], "Specific Date Case failed")
        self.assertEqual(rangeDates, [True, ['10-13-2021', '10-19-2021']], "Range Dates Case failed")
        
    def test_checkDates(self):
        realDates = clean.checkDates(['10-10-2021','10-10-2021','10-10-2021'])
        self.assertEqual(realDates, [True, ['10-10-2021','10-10-2021','10-10-2021']])

    def test_checkValidDate(self):
        check = clean.checkValidDate("1012121")
        checkTrue = clean.checkValidDate("10-20-2021")
        self.assertEqual(check, False, "False date went through!")
        self.assertEqual(checkTrue, True, "True date didn't work!")

    def test_dataQuery(self):
        data= clean.dataQuery(['combined'])
        wrongData= clean.dataQuery(['beep'])
        print(data)
        self.assertEqual([False, "Illegal data queries entered : beep"], wrongData)
        self.assertEqual([True, ['combined']], data, "Data did not register correctly!")

    def test_validType(self):
        noTypes = clean.validType(None)
        correctType = clean.validType('CSV')
        incorrectType = clean.validType('CST')
        self.assertEqual(False, noTypes, "No type was incorrect")
        self.assertEqual(True, correctType, "Correct type was marked incorrect")
        self.assertEqual(False, incorrectType, "Incorrect type was marked correct")
        
if __name__ == "__main__":
    unittest.main()