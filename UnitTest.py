import unittest
import workcheck

#05-10,07:20-13:50,00:30,0
class splitTester(unittest.TestCase):

    def setUp(self):
        self.splitting = workcheck.splitting()

    def testmain(self):
        self.string = "jeg er sej"
        self.splitReturn = self.splitting.main(self.string," ")
        self.listlength = len(self.splitReturn)
        self.assertIsInstance(self.splitReturn, list)
        self.assertEqual(self.listlength, 3)
        self.assertEqual(self.splitReturn[0],"jeg")
        self.assertEqual(self.splitReturn[1],"er")
        self.assertEqual(self.splitReturn[2],"sej")


class calculateTester(unittest.TestCase):
    def setUp(self):
        self.filing = workcheck.files()
        self.calculate = workcheck.calculating()
        self.filing.fileWrite("100.0","w")
        self.filing.fileWrite("6","a")
        self.filing.fileWrite("10.0","a")
        self.filing.fileWrite("20.0","a")
        self.filing.fileWrite(['2'],"a")
        self.filing.fileWrite("18:00-20:00","a")
        self.filing.fileWrite("30.0","a")
        self.filing.fileWrite(['3'],"a")
        self.filing.fileWrite("18:00-20:00","a")
        self.filing.fileWrite("True","a")

    def testweekDay(self):
        self.date = "05-05" #denne dato kombineret med året er en tirsdag
        self.year = 2020
        self.weekDayReturn = self.calculate.WeekdayCheck(self.date,self.year)
        self.assertIsInstance(self.calculate.dateSplit, list)
        self.assertIsInstance(self.weekDayReturn, int)
        self.assertEqual(self.weekDayReturn, 1)

#06-05,18:00-20:00,00:00,0
    def testaddPay(self):
        self.date = "05-05" #denne dato kombineret med året er en tirsdag som ligger uden for specialtid
        self.date2 = "06-05" #specialtid 1 onsdag
        self.date3 = "07-05" # specialtid 2 torsdag
        self.date4 = "10-05" # specialtid 3 søndag
        self.year = 2020
        self.shiftHours = "18:00-20:00" #en der er det samme som specialtid
        self.shiftHours2 = "18:10-19:10"# en imellem
        self.shiftHours3 = "18:00-21:00" # en imellem over
        self.shiftHours4 = "17:00-20:00" #en under imellem
        self.shiftHours5 = "17.00-21:00" #en under over
        self.bool1 = False
        self.bool2 = True
        #test none
        self.addPayReturn1 = self.calculate.addPayCheck(self.date,self.shiftHours,self.bool1,self.year)
        self.assertEqual(self.addPayReturn1, 0)
        #test holiday
        self.addPayReturn2 = self.calculate.addPayCheck(self.date,self.shiftHours,self.bool2,self.year)
        self.assertIsInstance(self.addPayReturn2, float)
        self.assertEqual(self.addPayReturn2, 20)
        #test specialtid 3 søndag
        self.addPayReturn3 = self.calculate.addPayCheck(self.date4,self.shiftHours,self.bool1,self.year)
        self.assertIsInstance(self.addPayReturn3, float)
        self.assertEqual(self.addPayReturn3, 20)
        #test onsdag samme
        self.addPayReturn4 = self.calculate.addPayCheck(self.date2,self.shiftHours,self.bool1,self.year)
        self.assertIsInstance(self.addPayReturn4, float)
        self.assertEqual(self.addPayReturn4, 40)
        #test onsdag imellem
        self.addPayReturn5 = self.calculate.addPayCheck(self.date2,self.shiftHours2,self.bool1,self.year)
        self.assertIsInstance(self.addPayReturn5, float)
        self.assertEqual(self.addPayReturn5, 20)
        #test onsdag imellem over
        self.addPayReturn6 = self.calculate.addPayCheck(self.date2,self.shiftHours3,self.bool1,self.year)
        self.assertIsInstance(self.addPayReturn6, float)
        self.assertEqual(self.addPayReturn6, 40)
        #test onsdag under imellem
        self.addPayReturn7 = self.calculate.addPayCheck(self.date2,self.shiftHours4,self.bool1,self.year)
        self.assertIsInstance(self.addPayReturn7, float)
        self.assertEqual(self.addPayReturn7, 40)
        #test onsdag under over
        self.addPayReturn8 = self.calculate.addPayCheck(self.date2,self.shiftHours5,self.bool1,self.year)
        self.assertIsInstance(self.addPayReturn8, float)
        self.assertEqual(self.addPayReturn8, 40)

        #test torsdag samme
        self.addPayReturn9 = self.calculate.addPayCheck(self.date3,self.shiftHours,self.bool1,self.year)
        self.assertIsInstance(self.addPayReturn9, float)
        self.assertEqual(self.addPayReturn9, 60)
        #test torsdag imellem
        self.addPayReturn10 = self.calculate.addPayCheck(self.date3,self.shiftHours2,self.bool1,self.year)
        self.assertIsInstance(self.addPayReturn10, float)
        self.assertEqual(self.addPayReturn10, 30)
        #test torsdag imellem over
        self.addPayReturn11 = self.calculate.addPayCheck(self.date3,self.shiftHours3,self.bool1,self.year)
        self.assertIsInstance(self.addPayReturn11, float)
        self.assertEqual(self.addPayReturn11, 60)
        #test torsdag under imellem
        self.addPayReturn12 = self.calculate.addPayCheck(self.date3,self.shiftHours4,self.bool1,self.year)
        self.assertIsInstance(self.addPayReturn12, float)
        self.assertEqual(self.addPayReturn12, 60)
        #test torsdag under over
        self.addPayReturn13 = self.calculate.addPayCheck(self.date3,self.shiftHours5,self.bool1,self.year)
        self.assertIsInstance(self.addPayReturn13, float)
        self.assertEqual(self.addPayReturn13, 60)


    def testholiday(self):
        self.holidayReturn1 = self.calculate.holidayCheck("1")
        self.holidayReturn2 = self.calculate.holidayCheck(1)
        self.holidayReturn3 = self.calculate.holidayCheck(2)
        self.assertEqual(self.holidayReturn1,True)
        self.assertEqual(self.holidayReturn2,True)
        self.assertEqual(self.holidayReturn3,False)

    def testtimeDif(self):
        self.timeDifReturn = self.calculate.timeDif("18:00","20:00")
        #self.assertIsInstance(self.timeDifReturn, 'datetime.timedelta')
        self.assertEqual(str(self.timeDifReturn),"2:00:00")

    def testtimeDecimal(self):
        self.timeDecimalReturn = self.calculate.timeDecimal("2:30:00")
        self.assertIsInstance(self.timeDecimalReturn, float)
        self.assertEqual(self.timeDecimalReturn, 2.5)

    def testoneDay(self):
        #if self.filing.fileRead(1) != "null":
        self.addPay = float(5)
        self.hourDecimal = float(2.5)
        self.pauseDecimal = float(0.5)
        self.oneDayReturn = self.calculate.oneDay(self.hourDecimal,self.pauseDecimal,self.addPay)
        self.assertIsInstance(self.oneDayReturn, tuple)
        self.assertEqual(self.oneDayReturn[0], self.filing.fileRead(1) * (self.hourDecimal - self.pauseDecimal) + self.addPay)
        self.assertIsInstance(self.oneDayReturn[0], float)
        self.assertEqual(self.oneDayReturn[1], self.pauseDecimal)
        self.assertIsInstance(self.oneDayReturn[1], float)
        self.assertEqual(self.oneDayReturn[2], self.hourDecimal)
        self.assertIsInstance(self.oneDayReturn[2], float)

    def testtotal(self):
        self.totalList1 = [1,2,3,4]
        self.totalList2 = [1,2,3,4]
        self.totalList3 = [1,2,3,4]
        self.totalReturn = self.calculate.total(self.totalList1,self.totalList2,self.totalList3)
        self.assertEqual(self.totalReturn[0], 10)
        self.assertIsInstance(self.totalReturn[0], float)
        self.assertEqual(self.totalReturn[1], 10)
        self.assertIsInstance(self.totalReturn[1], float)
        self.assertEqual(self.totalReturn[2], 10)
        self.assertIsInstance(self.totalReturn[2], float)

class fileTester(unittest.TestCase):
    def setUp(self):
        self.filing = workcheck.files()

    def testfileRead(self):
        self.assertIsInstance(self.filing.fileRead(1), float)
        self.assertIsInstance(self.filing.fileRead(2), int)
        self.assertIsInstance(self.filing.fileRead(3), float)
        self.assertIsInstance(self.filing.fileRead(4), float)
        self.assertIsInstance(self.filing.fileRead(5), list)
        self.assertIsInstance(self.filing.fileRead(6), str)
        self.assertIsInstance(self.filing.fileRead(7), float)
        self.assertIsInstance(self.filing.fileRead(8), list)
        self.assertIsInstance(self.filing.fileRead(9), str)



if __name__ == '__main__':
    unittest.main()
