from unittest import TestCase
from timeit import timeit as now

from strmath import Number


class TestStrmath(TestCase):
    def testInit(self):
        eleven = Number('11')
        self.assertIsNotNone(eleven, "eleven should be a Number instance")
        eleven_1 = Number('11010000000000000000000000000000', binary=True)
        self.assertIsNotNone(eleven_1, "eleven_1 should be a Number instance")
        self.assertEqual(eleven, eleven_1)

    def testValue(self):
        eleven = Number('11')
        self.assertEqual('11010000000000000000000000000000', eleven._value)

    def testNeg(self):
        self.assertEqual(Number('-3'), -Number('3'))

    def testAdd(self):
        eleven = Number('11')
        twelve = Number('12')
        self.assertTrue(Number('23'), eleven + twelve)

    def testMul(self):
        op1 = Number('123456')
        op2 = Number('654321')
        mod = Number('675')
        expected = Number(str(123456 * 654321 % 675))
        self.assertEqual(expected, op1.__mul__(op2, mod))
        op1 = Number('327')
        op2 = Number('765')
        expected = Number(str(327 * 765))
        self.assertEqual(expected, op1 * op2)

    def testDivmod(self):
        self.assertEqual((Number('11'), Number('8')), divmod(Number('140'), Number('12')))

    def testDiv(self):
        self.assertEqual(Number('11'), Number('140') // Number('12'))

    def testModulo(self):
        self.assertEqual(Number('8'), Number('140') % Number('12'))

    def testPow(self):
        base = Number('4020034')
        exponent = Number('168945678')
        mod = Number('75242567')
        n = pow(4020034, 168945678, 75242567)
        self.assertTrue(isinstance(n, int))
        expected = Number(str(n))
        self.assertTrue(isinstance(expected, Number))
        start = now()
        self.assertEqual(expected, pow(base, exponent, mod))
        print(now() - start)
