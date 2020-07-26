
"""
| This file is executed first when the rpncalc application is run by the user.
| USAGE:
| 
|   Interactive:
| 
|     rpncalc                         Launch in interactive mode
| 
|     example:
| 
|     rpncalc   
|     > 1 2 +    
|     3 > 5 +    
|     8 > quit   
| 
|   One Time Use:
| 
|     rpncalc [expression]            
|     
|     To evaluate a one-line expression
|     One can also excute several expressions in a pipeline 
|     by using the ',' operator to seperate them.
| 
|     examples:
| 
|     rpncalc 1 2 +
|     3
| 
|     rpncalc 1 2 +, 5 *
|     15
| 
| 
| NOTE: The expression should be supplied in the form of a string to the rpncalc.
"""

# import sys
import argparse

try:
    import calc
except ModuleNotFoundError:
    from rpn import calc
try:
    import config
except ModuleNotFoundError:
    from rpn import config

def main():
    arg_parser = argparse.ArgumentParser(description='Processes a rpn expression.')

    arg_parser.add_argument(
        '--version', '-v',action='store_true', default=False,
        help='Prints the version number and exits.')

    arg_parser.add_argument(
        'expression',
        nargs='*',
        help='Evaluates the expression in one time use format and exits.')

    args = arg_parser.parse_args()

    # if args.help:
    #     print ("\033[34m" + docs + "\033[0m")
    #     sys.exit()

    if args.version:
        from rpn import __version__
        print(config.bcolors.OKGREEN + __version__ + config.bcolors.ENDC)
    else:
        #print("~ Nums: {}".format(args.expression))
        if len(args.expression) > 0:
            # For one time use
            eval_string = ''
            for i in args.expression:
                eval_string += (i+" ")
            #print(eval_string)
            calc.one_time_use(eval_string)
        else:
            # For interactive use
            calc.interactive_use()

if __name__ == "__main__":
    main()
