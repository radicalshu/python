#!/usr/bin/env python
# code by SW
#for practice
import sys

def readfile(filename):
    f = file(filename)
    while True:
        line = f.readline()
        if len(line) == 0:
            break
        print line;
    f.close()

if len(sys.argv) < 2:
    print 'noting todo'
    sys.exit()
if sys.argv[1].startswith('--'):
    option = sys.argv[1][2:]
    if option == 'version':
        print 'Version beta'
    elif option == 'help':
        print ''' 
just like cat 
Options include:
--version   to show the version of cat.py
--help      Display the help'''
    else:
        print 'Wrong option'

else:
    for filename in sys.argv[1:]:
        readfile(filename)  
