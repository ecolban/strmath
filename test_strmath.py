from unittest import TestCase
from time import time as now

from strmath import StrNum


class TestStrmath(TestCase):

    def testInit(self):
        eleven = StrNum('11')
        self.assertIsNotNone(eleven, "eleven should be a Number instance")
        eleven_1 = StrNum('11010000000000000000000000000000', binary=True)
        self.assertIsNotNone(eleven_1, "eleven_1 should be a Number instance")
        self.assertEqual(eleven, eleven_1)

    def testValue(self):
        eleven = StrNum('11')
        self.assertEqual('11010000000000000000000000000000', eleven._value)

    def testNeg(self):
        self.assertEqual(StrNum('-3'), -StrNum('3'))

    def testAdd(self):
        eleven = StrNum('11')
        twelve = StrNum('12')
        self.assertEqual(eleven + twelve, StrNum('23'))

    def testGt(self):
        a = StrNum('-2')
        b = StrNum('-1')
        c = StrNum('0')
        d = StrNum('1')
        e = StrNum('2')
        self.assertTrue(a < b < c < d < e)

    def testMul(self):
        op1 = StrNum("-15")
        op2 = StrNum("17")
        mod = StrNum("20")
        self.assertEqual(op1.__mul__(op2, mod), StrNum(str(-15 * 17 % 20)))
        op1 = StrNum('123456')
        op2 = StrNum('654321')
        mod = StrNum('675')
        self.assertEqual(op1.__mul__(op2, mod), StrNum(str(123456 * 654321 % 675)))
        op1 = StrNum('327')
        op2 = StrNum('765')
        self.assertEqual(op1 * op2, StrNum(str(327 * 765)))

    def testDivmod(self):
        self.assertEqual(divmod(-StrNum('140'), StrNum('12')), (-StrNum('12'), StrNum('4')))

    def testDiv(self):
        self.assertEqual(StrNum('140') // StrNum('12'), StrNum('11'))

    def testModulo(self):
        self.assertEqual(StrNum('140') % StrNum('12'), StrNum('8'))

    def testPow(self):
        args = (740_227_090, 871_816_537, 1_073_058_648)
        n = pow(*args)
        self.assertTrue(isinstance(n, int))
        expected = StrNum(str(n))
        self.assertTrue(isinstance(expected, StrNum))
        start = now()
        str_num_args = (StrNum(str(a)) for a in args)
        self.assertEqual(pow(*str_num_args), expected)
        print(now() - start)

    def testRepr(self):
        n = StrNum('123456')
        self.assertEqual(repr(n), "StrNum('123456')")

    def testStr(self):
        n = StrNum('6543210')
        self.assertEqual(str(n), '6543210')
