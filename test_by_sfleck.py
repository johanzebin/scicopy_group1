# 2 inputs -> define a pattern, define a file
# grepy reads file and prints each line in which pattern 
# occurs (both can be given as regexp)
#
# grepy PATTERN FILE [FILE] [OPTIONS]
#
# grepy py*hon *.py 
# the line above searches for all matches 

import os 
import re #for regexp
import optparse #for parsing

# konstruktor definieren der irgendwie die signaturen 
# übernimmt und dann die funktion startet

# sowas?? 

for line in open("file"):
     if "search_string" in line:
        print line
        

def grepy(pattern, file)
    pattern = re.compile("pattern")
    file = open("file",'r')

# LOTSA SHIZTS

#os.chdir(path)
#Change the current working directory to path.
#
#os.getcwd()
#Return a string representing the current working directory.
#
#os.listdir(path)
#Return a list containing the names of the entries in the directory given by path. The list is in arbitrary order. It does not include the special entries '.' and '..' even if they are present in the directory.

