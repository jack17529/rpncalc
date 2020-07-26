"""
My very own execption class made just for this rpn calculator.
This file converts exceptions objects into beautiful strings using __str__
"""
try:
    import config
except ModuleNotFoundError:
    from rpn import config


class ZeroDivision:
    """This class handles Zero Division Error and returns relavent error string.
    """

    def __init__(self, name, msg):
        """
        Args:
            name (string): Name of the function.
            msg (string): Error message to be printed.
        """
        self.name, self.message = name, msg

    def __str__(self):
        return f"{config.bcolors.FAIL}ZeroDivisionError in {self.name} function. {self.message}. You can't divide by 0.{config.bcolors.ENDC}".format(
            self=self
        )


class Type:
    """Handles the Type Exceptions.
    """

    def __init__(self, name, msg, typ):
        """
        Args:
            name (string): Name of the function.
            msg (string): Error message to be printed.
            typ (string): the required type for the correct working.
        """
        self.name, self.message, self.type = name, msg, typ

    def __str__(self):
        return f"{config.bcolors.FAIL}TypeError in {self.name} function. The {self.message} should be {self.type}.{config.bcolors.ENDC}".format(
            self=self
        )


class Value:
    """Handles the Value Exceptions.
    """

    def __init__(self, name, msg):
        """
        Args:
            name (string): Name of the function.
            msg (string): Error message to be printed.
        """
        self.name, self.message = name, msg

    def __str__(self):
        return f"{config.bcolors.FAIL}ValueError in {self.name} function. {self.message}.{config.bcolors.ENDC}".format(
            self=self
        )


class ZeroRaisedToZero:
    """Handles my very own made error for the app, 0 raised to power of 0.
    """

    def __init__(self, name, msg):
        """
        Args:
            name (string): Name of the function.
            msg (string): Error message to be printed.
        """
        self.name, self.message = name, msg

    def __str__(self):
        return f"{config.bcolors.FAIL}LimitError in {self.name} function. {self.message}. 0 raised to power of 0 is undefined limit.{config.bcolors.ENDC}".format(
            self=self
        )


class Infinite:
    """Handles my very own made error for the app, when the output is infinite.
    The calculations with infinity along with limits is not avialable in this version.
    """

    def __init__(self, name, msg):
        """
        Args:
            name (string): Name of the function.
            msg (string): Error message to be printed.
        """
        self.name, self.message = name, msg

    def __str__(self):
        return f"{config.bcolors.FAIL}InfiniteError in {self.name} function. {self.message}. Infinity is undefined.{config.bcolors.ENDC}".format(
            self=self
        )


class ConversionToBase10:
    """Handles my very own made error for the app, 
    when the output can't be converted to base 10.
    """

    def __init__(self, msg, typ):
        """
        Args:
            name (string): Name of the function.
            msg (string): Error message to be printed.
            typ (string): the required type for the correct working.
        """
        self.message, self.type = msg, typ

    def __str__(self):
        return f"{config.bcolors.FAIL}Conversion to Base 10 error. The {self.message} should be {self.type}.{config.bcolors.ENDC}".format(
            self=self
        )


class OneWordCommand:
    """Handles my very own made error for the app, 
    when we supply other commands to one command functions.
    """

    def __init__(self, name):
        """
        Args:
            name (string): Name of the function.
        """
        self.name = name

    def __str__(self):
        return f"{config.bcolors.FAIL}One word command error. The string to be parsed can't contain anything else except {self.name}.{config.bcolors.ENDC}".format(
            self=self
        )


class Overflow:
    """Handles the math Overflow Exception, 
    when the output overflows.
    """

    def __init__(self, name, msg):
        """
        Args:
            name (string): Name of the function.
            msg (string): Error message to be printed.
        """
        self.message, self.name = msg, name

    def __str__(self):
        return f"{config.bcolors.FAIL}Negative Value Overflow Error in {self.name} function. {self.message}.{config.bcolors.ENDC}".format(
            self=self
        )
