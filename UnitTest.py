import unittest
import workcheck

#05-10,07:20-13:50,00:30,0

class unittest(unittest.TestCase):

    def fileReadTest(self):
        self.line1 = self.assertIsInstance(fileRead(1), float)
        self.line2 = self.assertIsInstance(fileRead(2), float)
        self.line3 = self.assertIsInstance(fileRead(3), float)
        self.line4 = self.assertIsInstance(fileRead(4), float)
        self.line5 = self.assertIsInstance(fileRead(5), float)
        self.line6 = self.assertIsInstance(fileRead(6), float)
        self.line7 = self.assertIsInstance(fileRead(7), float)
        self.line8 = self.assertIsInstance(fileRead(8), float)
        self.line9 = self.assertIsInstance(fileRead(9), float)
        self.line10 = self.assertIsInstance(fileRead(10), float)
        print(self.line1)

    def calculateTest(self):
        pass

    def structureTest(self):
        pass


if __name__ == '__main__':
    unittest.main()
