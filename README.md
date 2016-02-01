# strmath

A simple Python project where numbers are represented by strings. No ints, longs, or floats are used, 
nor any function that returns a value of any of these types. Computations are performed through string 
manipulations only. No integers are used in indexing strings or arrays.

Numbers are signed integers represented as 32-bit binary strings. Overflow and underflow may occur just as
in ordinary 32-bit integer computations. Operations supported are: negation, addition, subtraction, multiplication,
division, modulo, divmod, and left and right shifts. The operators +, -, *, /, %, <<, and >> may be used to invoke 
these operations. Comparisons may be invoked using <, <=, ==, >=, and >.   

Example:
    
    >>> print(Number('13') * Number('1071'))
    13923
    >>> print((Number('-1024') >> Number('2')) * Number('12') + Number('15'))
    -3057
    >>> print('q = %s, r = %s' % divmod(Number('21809'), Number('101')))
    q = 215, r = 94

These calculations may be verified using ordinary arithmetic:

    >>> 13 * 1071
    13923
    >>> (-1024 >> 2) * 12 + 15
    -3057
    >>> divmod(21809, 101)
    (215, 94)

The code also provides example implementations of the functions `multmod` and `powmod`, which are identical to the 
implementations of these functions using ordinary arithmetic except that the `strmath` equivalents of certain 
constants are used. For example, `zero` and `one` is used instead of `0` and `1`. Note that `zero` is defined as
`Number('0')` and `one` is defined as `Number('1')`.

Example:

    >>> print(powmod(Number('23'), Number('12345'), Number('700')))
    43

This result may be verified using the built-in function `pow`:

    >>> pow(23, 12345, 700)
    43

