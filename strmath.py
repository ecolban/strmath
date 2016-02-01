'''
Created on Jan 31, 2016

@author: Erik Colban
'''
from pip._vendor.requests.packages.chardet.utf8prober import ONE_CHAR_PROB
class Number:
    
    # Defining 32-bit numbers

    digit_to_binary = {  
        '0':'00000000000000000000000000000000', 
        '1':'00000000000000000000000000000001', 
        '2':'00000000000000000000000000000010', 
        '3':'00000000000000000000000000000011', 
        '4':'00000000000000000000000000000100', 
        '5':'00000000000000000000000000000101', 
        '6':'00000000000000000000000000000110', 
        '7':'00000000000000000000000000000111', 
        '8':'00000000000000000000000000001000', 
        '9':'00000000000000000000000000001001'}

    binary_to_digit = {b:d for d, b in digit_to_binary.items()}

    def __init__(self, s, dec=True):
        # should have validated s, but trusting the client instead
        if not dec: self.value = s
        elif len(s) == 1: self.value = Number.digit_to_binary[s]
        else:
            n = zero
            sgn = one
            for d in s:
                if d == '-': sgn = -sgn
                else:
                    n *= ten
                    n += Number(d)
            self.value = (sgn * n).value
                     

        
    def __add__(self, other):
        s = zip(self.value, other.value)
        value = ''
        carry = '0'
        for x in reversed(s):
            if x == ('0', '0'):
                value = carry + value
                carry = '0'
            elif x == ('1', '1'):
                value = carry + value
                carry = '1'
            elif carry == '1':
                value = '0' + value
            else:
                value = '1' + value
        return Number(value, dec=False)



    def __lshift__(self, other):
        b = one
        s = self
        while b <= other:
            s = s + s
            b = b + one
        return s

    def __rshift__(self, other):
        b = one
        s = self.value
        c = '1' if self.__is_negative() else '0'
        while b <= other:
            s = c + s
            b += one
        # using zip to truncate s to the length of zero.value
        r = zip(s, zero.value)
        s, _ = zip(*r)
        return Number(''.join(s), dec=False)

    def __neg__(self):
        one_complement = ''.join('1' if c == '0' else '0' for c in self.value)
        return Number(one_complement, dec=False) + one

    def __sub__(self, other):
        return self + -other

    def __is_negative(self):
        return next(iter(self.value)) == '1'

    def __abs__(self):
        if self.__is_negative(): return -self
        else: return self

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return (other - self).__is_negative()

    def __ge__(self, other):
        return self == other or self > other

    def __mul__(self, other):
        if self.__is_negative():
            return -(-self * other)
        s1 = self
        b = one
        result = zero
        while b <= s1:
            b <<= one
        while b > one:
            b >>= one
            result <<= one
            if s1 >= b:
                s1 -= b
                result += other
        return result

    def __divmod__(self, other):
        if self.__is_negative() and other.__is_negative():
            q, r = divmod(-self, -other)
            return q, -r
        elif self.__is_negative():
            q, r = divmod(-self, other)
            q, r = -q, -r
            if r != zero:
                r += other
                q -= one
            return q, r
        elif other.__is_negative():
            q, r = divmod(self, -other)
            q = -q
            if r != zero:
                r += other
                q -= one
            return q, r
        else: # neither self nor other is negative
            s1 = self
            b = one
            q, r = zero, zero
            while s1 >= b:
                b <<= one
            while b > one:
                b >>= one
                q, r = q << one, r << one
                if s1 >= b:
                    s1 -= b
                    r += one
                if r >= other:
                    r -= other
                    q += one
            return (q, r)

    def __div__(self, other):
        q, _ = divmod(self, other)
        return q

    def __mod__(self, other):
        _, r = divmod(self, other)
        return r


    def __str__(self):
        if self == zero: return '0'
        if self < zero: return '-' + str(-self)
        result = ""
        s = self
        while s > zero:
            s, r = divmod(s, ten)
            result = Number.binary_to_digit[r.value] + result
        return result


zero = Number('0')
one = Number('1')
ten = Number('5') << one

def multmod(m, n, mod):
    b, p = one, zero
    while b <= n: b <<= one
    while b > one:
        b >>= one
        p <<= one
        if p >= mod: p -= mod
        if b <= n:
            n -=b
            p += m
            if p >= mod: p -= mod
    return p

def powmod(m, n, mod):
    b, p = one, one
    while b <= n: b <<= one
    while b > one:
        b >>= one
        p = multmod(p, p, mod)
        if b <= n:
            n -= b
            p = multmod(p, m, mod)
    return p
    




        



    


                  
    
    


        


    
    
                
    
