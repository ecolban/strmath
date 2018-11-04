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


def last(s):
    # return s[-1]
    return next(reversed(s))


class StrNum(object):
    """
    Created on Jan 31, 2016

    @author: Erik Colban
    """

    # Defining 32-bit numbers in little-endian
    digit_to_binary = {
        '0': '00000000000000000000000000000000',
        '1': '10000000000000000000000000000000',
        '2': '01000000000000000000000000000000',
        '3': '11000000000000000000000000000000',
        '4': '00100000000000000000000000000000',
        '5': '10100000000000000000000000000000',
        '6': '01100000000000000000000000000000',
        '7': '11100000000000000000000000000000',
        '8': '00010000000000000000000000000000',
        '9': '10010000000000000000000000000000'}

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
            for x in zip(self._value, other._value):
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

        return StrNum(''.join(bit_gen()), binary=True)

    def _incr(self):
        # return self + one

        def bit_gen():
            found_0 = False
            for c in self._value:
                if found_0:
                    yield c
                elif c == '0':
                    found_0 = True
                    yield '1'
                else:
                    yield '0'

        return StrNum(''.join(bit_gen()), binary=True)

    def _decr(self):
        # return self - one

        def bit_gen():
            found_1 = False
            for c in self._value:
                if found_1:
                    yield c
                elif c == '1':
                    found_1 = True
                    yield '0'
                else:
                    yield '1'

        return StrNum(''.join(bit_gen()), binary=True)

    def __neg__(self):
        # one_complement = ''.join('1' if c == '0' else '0' for c in self._value)
        # return StrNum(one_complement, binary=True) + one

        def bit_gen():
            found_1 = False
            for c in self._value:
                if found_1:
                    yield '1' if c == '0' else '0'
                elif c == '1':
                    found_1 = True
                    yield '1'
                else:
                    yield '0'

        return StrNum(''.join(bit_gen()), binary=True)

    def __sub__(self, other):
        return self + -other

    def __is_negative(self):
        return last(self._value) == '1'

    def __abs__(self):
        if self.__is_negative():
            return -self
        else:
            return self

    def __gt__(self, other):
        # return (other - self).__is_negative()
        z = zip(reversed(self._value), reversed(other._value))
        self_sign, other_sign = next(z) # sign bits
        if self_sign != other_sign: return self_sign == '0'
        try:
            x, _ = next((x, y) for x, y in z if x != y)
            return x == '1'
        except StopIteration:
            return False

    def __ge__(self, other):
        return not other.__gt__(self)

    def __lt__(self, other):
        return other.__gt__(self)

    def __le__(self, other):
        return not self.__gt__(other)

    def __lshift__(self, other):
        s = self._value
        if other == one:
            s = truncate_right('0' + s)
            return StrNum(s, binary=True)
        b = one
        while b <= other:
            s = truncate_right('0' + s)
            b = b._incr()
        return StrNum(s, binary=True)

    def __rshift__(self, other):
        s = self._value
        c = last(s)
        if other == one:
            s = truncate_right(s + c)
            return StrNum(s, binary=True)
        b = one
        while b <= other:
            s = truncate_left(s + c)
            b = b._incr()
        return StrNum(s, binary=True)

    # def __mul__(self, other):
    #     if self.__is_negative():
    #         return -(-self).__mul__(other)
    #
    #     result = zero
    #     for b in reversed(self._value):
    #         result <<= one
    #         if b == '1':
    #             result += other
    #     return result

    def __mul__(self, other, mod=None):
        """mod is None or positive"""
        if mod and (self.__is_negative() or self >= mod or other.__is_negative() or other >= mod):
            return (self % mod).__mul__(other % mod, mod)

        if self.__is_negative():
            return -(-self).__mul__(other, mod)

        result = zero
        for b in reversed(self._value):
            result <<= one
            if mod and result >= mod: result -= mod
            if b == '1': result += other
            if mod and result >= mod: result -= mod
        return result

    def __divmod__(self, other):
        if self >= zero and other > zero:
            q, r = zero, zero
            for b in reversed(self._value):
                q, r = q << one, r << one
                if b == '1':
                    r = r._incr()
                if r >= other:
                    r -= other
                    q = q._incr()
            return q, r
        elif self < zero and other > zero:
            q, r = divmod(-self, other)
            q, r = -q, -r
            if r != zero:
                r += other
                q = q._decr()
            return q, r
        elif self >= zero and other < zero:
            q, r = divmod(self, -other)
            q = -q
            if r != zero:
                r += other
                q = q._decr()
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
        for b in reversed(n._value):
            p = p.__mul__(p, mod)
            if b == '1':
                p = p.__mul__(self, mod)
        return p

    def __repr__(self):
        return "StrNum('%s')" % str(self)

    def __str__(self):
        if self == zero: return '0'
        if self < zero: return '-' + str(-self)
        result = ""
        s = self
        while s > zero:
            s, r = s.__divmod__(ten)
            result = StrNum.binary_to_digit[r._value] + result
        return result


zero = StrNum('0')
one = StrNum('1')
ten = StrNum('01010000000000000000000000000000', binary=True)
