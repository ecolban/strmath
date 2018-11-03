def truncate_left(s):
    # return s[1:]
    g = (c for c in s)
    next(g)
    return ''.join(g)


def truncate_right(s):
    # return s[:-1]
    g = reversed(s)
    next(g)
    return ''.join(reversed(list(g)))


def first(s):
    # return s[0]
    return next(c for c in s)


class StrNum(object):
    """
    Created on Jan 31, 2016

    @author: Erik Colban
    """

    # Defining 32-bit numbers in big-endian
    digit_to_binary = {
        '0': '00000000000000000000000000000000',
        '1': '00000000000000000000000000000001',
        '2': '00000000000000000000000000000010',
        '3': '00000000000000000000000000000011',
        '4': '00000000000000000000000000000100',
        '5': '00000000000000000000000000000101',
        '6': '00000000000000000000000000000110',
        '7': '00000000000000000000000000000111',
        '8': '00000000000000000000000000001000',
        '9': '00000000000000000000000000001001'}

    binary_to_digit = {b: d for d, b in digit_to_binary.items()}

    def __init__(self, s, binary=False):
        # should have validated s, but trusting the client instead
        if binary:
            self._value = s
        elif s in StrNum.digit_to_binary:
            self._value = StrNum.digit_to_binary[s]
        else:
            n = zero
            sgn = one
            for d in s:
                if d == '-':
                    sgn = -sgn
                else:
                    n *= ten
                    n += StrNum(d)
            self._value = (sgn * n)._value

    def __eq__(self, other):
        return self._value == other._value

    def __ne__(self, other):
        return self._value != other._value

    def __hash__(self):
        return hash(self._value)

    def __add__(self, other):

        def bit_gen():
            carry = '0'
            for x in zip(reversed(self._value), reversed(other._value)):
                if x == ('0', '0'):
                    yield carry
                    carry = '0'
                elif x == ('1', '1'):
                    yield carry
                    carry = '1'
                elif carry == '1':
                    yield '0'
                else:
                    yield '1'

        return StrNum(''.join(reversed(list(bit_gen()))), binary=True)

    def _is_negative(self):
        return first(self._value) == '1'

    def __neg__(self):
        one_complement = ''.join('1' if c == '0' else '0' for c in self._value)
        return StrNum(one_complement, binary=True) + one

    def __sub__(self, other):
        return self + -other

    def __gt__(self, other):
        return (other - self)._is_negative()

    def __ge__(self, other):
        return self == other or self > other

    def __lt__(self, other):
        return (self - other)._is_negative()

    def __le__(self, other):
        return self == other or self < other

    def __abs__(self):
        if self._is_negative():
            return -self
        else:
            return self

    def __lshift__(self, other):
        s = self._value
        b = zero
        while b < other:
            s = truncate_left(s + '0')
            b = b + one
        return StrNum(s, binary=True)

    def __rshift__(self, other):
        s = self._value
        c = first(s)
        b = zero
        while b < other:
            s = truncate_right(c + s)
            b += one
        return StrNum(s, binary=True)

    # def __mul__(self, other):
    #     if self._is_negative():
    #         return -(-self).__mul__(other)
    #
    #     result = zero
    #     for b in self._value:
    #         result <<= one
    #         if b == '1':
    #             result += other
    #     return result

    def __mul__(self, other, mod=None):
        """mod is None or positive"""
        if mod and (self._is_negative() or self >= mod or other._is_negative() or other >= mod):
            return (self % mod).__mul__(other % mod, mod)

        if self._is_negative():
            return -(-self).__mul__(other, mod)

        result = zero
        for b in self._value:
            result <<= one
            if mod and result >= mod: result -= mod
            if b == '1':
                result += other
            if mod and result >= mod: result -= mod
        return result

    def __divmod__(self, other):
        if self >= zero and other > zero:
            q, r = zero, zero
            for b in self._value:
                q, r = q << one, r << one
                if b == '1':
                    r += one
                if r >= other:
                    r -= other
                    q += one
            return q, r
        elif self < zero and other > zero:
            q, r = divmod(-self, other)
            q, r = -q, -r
            if r != zero:
                r += other
                q -= one
            return q, r
        elif self >= zero and other < zero:
            q, r = divmod(self, -other)
            q = -q
            if r != zero:
                r += other
                q -= one
            return q, r
        elif self < zero and other < zero:
            q, r = divmod(-self, -other)
            return q, -r
        else:
            raise ArithmeticError

    def __floordiv__(self, other):
        q, _ = divmod(self, other)
        return q

    def __mod__(self, other):
        _, r = divmod(self, other)
        return r

    def __pow__(self, n, mod=None):
        if mod and self >= mod:
            return pow((self % mod), n, mod)
        p = one
        for b in n._value:
            p = p.__mul__(p, mod)
            if b == '1':
                p = p.__mul__(self, mod)
        return p

    def __str__(self):
        if self == zero: return '0'
        if self < zero: return '-' + str(-self)
        result = ""
        s = self
        while s > zero:
            s, r = s.__divmod__(ten)
            result = StrNum.binary_to_digit[r._value] + result
        return result

    def __repr__(self):
        return "StrNum('%s')" % str(self)


zero = StrNum('0')
one = StrNum('1')
ten = StrNum('00000000000000000000000000001010', binary=True)
