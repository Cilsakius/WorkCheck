import unittest
import workcheck

#05-10,07:20-13:50,00:30,0
class splitTester(unittest.TestCase):

    def setUp(self):
        self.splitting = workcheck.splitting()

    def mainTest(self):
        self.string = "jeg er sej"
        self.splitReturn = self.splitting(self.string," ")
        self.listlength = len(self.splitReturn)
        self.assertIsInstance(self.splitReturn, list)
        self.assertEqual(self.listlength, 3)
        self.assertEqual(self.splitReturn[0],"jeg")
        self.assertEqual(self.splitReturn[1],"er")
        self.assertEqual(self.splitReturn[2],"sej")


class calculateTester(unittest.TestCase):
    def setUp(self):
        self.calculate = workcheck.calculate()
        self.filing = workcheck.filing()

    def weekDayTest(self):
        self.date = "05-05" #denne dato kombineret med året er en tirsdag
        self.year = 2020
        self.weekDayReturn = self.calculate.WeekdayCheck(self.date,self.year)
        self.assertIsInstance(self.calculate.dateSplit, list)
        self.assertIsInstance(self.weekDayReturn, int)
        self.assertEqual(self.weekDayReturn, 1)

    def addPayTest(self):
        self.date = "05-05" #denne dato kombineret med året er en tirsdag
        self.year = 2020
        self.shiftHours = "18:00-20:00"
        self.bool1 = False
        self.addPayReturn = self.calculate.addPayCheck(self.date,self.shiftHours,self.bool1,self.year)
        self.assertIsInstance(self.addPayReturn, float)

    def holidayTest(self):
        self.holidayReturn1 = self.calculate.holidayCheck("1")
        self.holidayReturn2 = self.calculate.holidayCheck(1)
        self.holidayReturn3 = self.calculate.holidayCheck(2)
        self.assertEqual(self.holidayReturn1,True)
        self.assertEqual(self.holidayReturn2,True)
        self.assertEqual(self.holidayReturn3,False)

    def timeDifTest(self):
        self.timeDifReturn = self.calculate.timeDif("18:00","20:00")
        self.assertEqual(self.timeDifReturn, "2:00")
        self.assertIsInstance(self.timeDifReturn, 'datetime.timedelta')

    def timeDecimalTest(self):
        self.timeDecimalReturn = self.calculate.timeDecimal("2:30:00")
        self.assertIsInstance(self.timeDecimalReturn, float)
        self.assertEqual(self.timeDecimalReturn, 2.5)

    def oneDayTest(self):
        if self.filing.fileRead(1) != "null":
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

    def totalTest(self):
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

class filingTester(unittest.TestCase):
    def setUp(self):
        self.filing = workcheck.filing()

    def fileReadTest(self):
        try:
            self.checkFile = open("settings.txt", "r")
        except FileNotFoundError:
            self.assertEqual(self.filing.fileRead(1), None)
        else:
            if self.filing.fileRead(10) == "True\n":
                self.assertIsInstance(self.filing.fileRead(1), float)
                if self.filing.fileRead(2) != "null":
                    self.assertIsInstance(self.filing.fileRead(2), int)
                    self.assertIsInstance(self.filing.fileRead(3), float)
                if self.filing.fileRead(4) != "null":
                    self.assertIsInstance(self.filing.fileRead(4), float)
                    self.assertIsInstance(self.filing.fileRead(5), list)
                    self.assertIsInstance(self.filing.fileRead(6), str)
                    if self.filing.fileRead(7) != "null":
                        self.assertIsInstance(self.filing.fileRead(7), float)
                        self.assertIsInstance(self.filing.fileRead(8), list)
                        self.assertIsInstance(self.filing.fileRead(9), str)
        #self.line2 = self.assertIsInstance(fileRead(2), float)
        #self.line3 = self.assertIsInstance(fileRead(3), float)
        #self.line4 = self.assertIsInstance(fileRead(4), float)
        #self.line5 = self.assertIsInstance(fileRead(5), float)
        #self.line6 = self.assertIsInstance(fileRead(6), float)
        #self.line7 = self.assertIsInstance(fileRead(7), float)
        #self.line8 = self.assertIsInstance(fileRead(8), float)
        #self.line9 = self.assertIsInstance(fileRead(9), float)
        #self.line10 = self.assertIsInstance(fileRead(10), float)
        #print(self.line1)



if __name__ == '__main__':
    unittest.main()
