""" 
| Should be used to install a package locally.
| NOTE: The package is owned by Shivam Sharma(jack17529).
"""

from setuptools import setup

import os
thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()
        
        
setup(
	name='rpncalc',
	version='1.0.0',
	description='Best rpn calculator!',
	author="Shivam Sharma",
    author_email="15ucs130@lnmiit.ac.in",
    install_requires=install_requires,
	py_modules=["io","config","calc","custom_errors","lexer"],
	packages = ["rpn"],
    entry_points = { 
            'console_scripts': [
                'rpncalc = rpn.io:main'
            ] 
    },
    python_requires="==3.6.9",
    #zip_safe = False
)
