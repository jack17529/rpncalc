# rpncalc

Best RPN calculator on the net!  
This is the version 1.0.0 of rpncalc and is licenced under GPL V3. This is a Python 3.6.9 project following the PEP 8 conventions, made with care in vscode(the newest version). The app gets installed in the form of a cli package, with the help of the setup.py file present in the root directory of the project. Pylint is used for Python 3 style. Google docstrings are used for comments in the project. Black and autopep8 is used for auto formatting. Okay, vulture was used for dead code removal, but there wasn't any dead code :P  
I have tried to make the most user friendly rpn calculator, which is robust and maintainable at the same time. Please install/use the rpncalc project exactly the way as it is written in the respective topics below. Please use vscode to view the code. Please put a file named .rpnrc in your home directory, if you want to modify the configuration settings.

## Functionalities

### Command Line

This is the command line help from our reference implementation:

    USAGE:

      rpncalc                                   Launch in interactive mode
      rpncalc [expression]                      Evaluate a one-line expression
      rpncalc [expression1] , [expression2]     One can also excute several expressions in a pipeline by using the ',' operator.

    RC FILE

      rpncalc will execute the contents of ~/.rpnrc at startup if it exists.

    EXAMPLES
    
      rpncalc 1 2 + 3 + 4 + 5 +              => 15
      rpncalc pi cos                         => -1.0
      rpncalc                                => interactive mode

### Command Set

    Arithmetic Operators

      +          Add
      -          Subtract
      *          Multiply
      /          Divide
      cla        Clear the stack and variables
      clr        Clear the stack
      clv        Clear the variables
      !          Boolean NOT
      !=         Not equal to
      %          Modulus
      ++         Increment
      --         Decrement

    Bitwise Operators

      &          Bitwise AND
      |          Bitwise OR
      ^          Bitwise XOR
      ~          Bitwise NOT
      <<         Bitwise shift left
      >>         Bitwise shift right

    Boolean Operators

      &&         Boolean AND
      ||         Boolean OR
      ^^         Boolean XOR

    Comparison Operators

      <          Less than
      <=         Less than or equal to
      ==         Equal to
      >          Greater than
      >=         Greater than or equal to

    Trigonometric Functions

      acos       Arc Cosine
      asin       Arc Sine
      atan       Arc Tangent
      cos        Cosine
      cosh       Hyperbolic Cosine
      sin        Sine
      sinh       Hyperbolic Sine
      tanh       Hyperbolic tangent

    Numeric Utilities

      ceil       Ceiling
      floor      Floor
      round      Round
      ip         Integer part
      fp         Floating part
      sign       Push -1, 0, or 0 depending on the sign
      abs        Absolute value
      max        Max
      min        Min

    Display Modes

      hex        Switch display mode to hexadecimal
      dec        Switch display mode to decimal (default)
      bin        Switch display mode to binary
      oct        Switch display mode to octal

    Constants

      e          Push e
      pi         Push Pi
      rand       Generate a random number

    Mathematic Functions

      exp        Exponentiation
      fact       Factorial
      sqrt       Square Root
      ln         Natural Logarithm
      log        Logarithm
      pow        Raise a number to a power

    Networking

      hnl        Host to network long
      hns        Host to network short
      nhl        Network to host long
      nhs        Network to host short

    Stack Manipulation

      pick       Pick the -n'th item from the stack
      repeat     Repeat an operation n times, e.g. '3 repeat +'
      depth      Push the current stack depth
      drop       Drops the top item from the stack
      dropn      Drops n items from the stack
      dup        Duplicates the top stack item
      dupn       Duplicates the top n stack items in order
      roll       Roll the stack upwards by n
      rolld      Roll the stack downwards by n
      stack      Toggles stack display from horizontal to vertical
      swap       Swap the top 2 stack items

    Macros and Variables

      macro      Defines a macro, e.g. 'macro kib 1024 *'
      x=         Assigns a variable, e.g. '1024 x='

    Other

      help       Print the help message
      exit       Exit the calculator



## Installation

1. Unzip the repository. 
2. `cd` inside the repository.
3. Install the package using `pip3 install .`
4. Uninstall the package using `pip3 uninstall rpncalc`

## For one time usage

1. `set -f` (to disable glob)
2. Use `rpncalc 2 3 *, 4 *`
3. `set +f`

## Tests

The test are written using `pytest` and `unittest`
See the tests present in `test` directory or just eun them using `pytest` command.

## Docs

The docs are generated by `sphinx`.
See the docs present in `docs/build/html/index.html`
