#!/usr/bin/env python
# -*- coding: utf-8 -*-

# copyright michael rausch 17.05.2011
# mail: mrausch@uos.de
# University of Osnabrueck
# Homework 1 for the SciCoPy Course SS2011
 
import re, os
from optparse import OptionParser

def main():
    # Usage syntax:
    # grepy PATTERN FILE [FILE] [Options]
    # Command line args:
    # -c --color: print matches in color
    # -h -? --help: print help (automatic optparse?). also print this with no args
    # -n --line-number: prefix output lines with linenumber
    # -f --filenames: print filenames before occurences
    # -R --recursive: recursively process directories
    # -v: Print author details and version number
        
    # set usage info string and version string and create optparser
    usage = "%prog PATTERN FILE [FILE] [Options]"
    version = "%prog 0.1-mr"
    desc = "Finds and outputs patterns in specified file(s)" 
    parser = OptionParser(usage=usage, version=version, description=desc, add_help_option=False)
    # we suppress adding the help option to manually set it later

    # we're gonna overwrite --version, so make optparse stop moaning
    # this will also allow us to print --version at the end of the option list
    # by default, optparse puts this at the top of the option list, which is ugly
    parser.set_conflict_handler(handler="resolve")

    parser.add_option("-c", "--color", action="store_true", dest="color", help="Highlight pattern matches with color")
    parser.add_option("-h", "-?", "--help", action="help", help="Display this help page") # define the custom help switch
    parser.add_option("-n", "--line-numbers", action="store_true", dest="println", help="Print line-numbers of matches")
    parser.add_option("-f", "--filenames", action="store_true", dest="printfn", help="Print file names before matches")
    parser.add_option("-R", "--recursive", action="store_true", dest="recursive", help="Recursively process directories in the file list")
    parser.add_option("-v", "--version", action="version", help="Show author and version information and exit.")

    (options, args) = parser.parse_args() # get options and arguments from argv 

    if len(args) < 2: # print usage information if no or too less arguments are supplied
        parser.print_help() # print usage info
        exit(0) # and quit

    pattern = args[0] # first argument is the regex pattern
    #reg = re.compile(pattern)
    files = args[1:] # all other arguments are filenames
    
    grepy(files,pattern,options)
    
def grepy(files,pattern,options):
    # iterate over the filenames
    for filename in files:
        if os.path.isdir(filename):
            if options.recursive:
                # generate a list of subfiles, joining the current directory path and its sub-entries
                subfiles = [os.path.join(filename,entry) for entry in os.listdir(filename)]
                grepy(subfiles,pattern,options) # recurse over the files of the directory
            continue # ...skip the directory, either because we are done recursing, or we are not working recursive at all
       
        with open(filename) as infile: # file handles implement context manager for exceptions and stuff, see session 2 slide 21            
            lines = infile.readlines() # get all the lines. Yes, ALL the lines.
            for linenumber,line in enumerate(lines): # we want the line numbers too, see session 3 slide 29
                match = re.search(pattern,line) # check if the line matches the pattern
                if match:
                    prepend = ""
                    if options.printfn:
                        prepend = filename + ":"
                    if options.println:
                        prepend = prepend + str(linenumber+1) + ":"                        
                    # this is ugly, but currently I don't have an idea how to do it different
                    if options.color: # wrap some magic line chars for green color around the matched pattern
                        print prepend + re.sub(match.group(0), "\033[92m"+match.group(0)+"\033[0m", line.strip())
                        # see also: http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
                    else:
                        print prepend + line.strip() # simply print                                         
                # done with the line
            # done with the the file
                    
if __name__ == '__main__': main()