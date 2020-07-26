""" $ python3 rpn/io.py "macro x 10 10 *, pi x *"
Undefined variable or macro name 'macro'
Undefined variable or macro name 'x'
Syntax error at EOF
Undefined variable or macro name 'x' """

""" python3 rpn/io.py "2 3 +,4 4 2     repeat +"
repeat can't be used with floats. """

""" $ python3 rpn/io.py "2 3 +,4 4 + +"           
Syntax error at '+'
5 """

""" $ python3 rpn/io.py "2 3 +,4 4 2 repeat +"
Syntax error at '+'
5 """

""" 12.346 0.2 > .1 +
Illegal character '.'
Illegal character '.' """

""" > 2.5 round
2 > 3.5 round
2 4 > 2.5 floor """

""" -0.82704207469154 > sqrt
ValueError in Square root function. It works only for non negative numbers.
1 >  """

""" > 1.2
0b1 > 1 
0b1 0b1 """

""" > 1 ~
-2 > 0 ~
-2 -1 > bin
-2 -1 > 1/-/
-2 -1 -0b1 > ==
Syntax error at '-'
-2 -1 -0b1 >  """

""" > 1.00/-/ 0.00 min
-1.0 > 2 max
Syntax error at 'max'
-1.0 > """

""" -1.0 2 > 0 pick 
Traceback (most recent call last):
  File "/home/faith/Downloads/Calc-master/calc4.py", line 1019, in <module>
    config.st.append(config.st.pop(len(config.st)-(int(arr2[i-1]))))
IndexError: pop index out of range """

""" 0.199999 > 1.2 1.0 -
0.199999 0.199999 > """

""" > deg
> 90 cos
6.123233995736766e-17  """

""" 6.520904391968161e+51 6.520904391968254e+51 > +
Syntax error at EOF """

""" 1 2 3 4 > repeat dup
1 2 3 3 3 3 >  """

""" 0b11111111 > repeat dup
Traceback (most recent call last):
  File "/home/faith/Downloads/Calc-master/calc4.py", line 847, in <module>
    config.st.append(config.st[len(config.st)-1])
IndexError: list index out of range """

""" 69 1 2 > stack


69
1
2
> 2


69
1
2
2
> 
 """

""" [ x = 5354 y = 5339 z = 15 ] 0b1010011101010 > repeat dup
repeat can only be used with positive integers. """

""" > 0
0 > 0
0 0 > 0 repeat drop
Error: wrong use of operators in expression
0 >  """

""" > 0
0 > 0
0 0 > repeat dup """
