#!/usr/bin/env python
# -*- coding: utf-8 -*-

# copyright michael rausch 17.05.2011
# mail: mrausch@uos.de
# University of Osnabrueck
# Homework 1 for the SciCoPy Course SS2011

import re, os, time
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
    start_time = time.clock()
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

    parser.add_option("-c", "--color", action="store_true", dest="color", \
                       help="Highlight pattern matches with color")
    # define the custom help switch
    parser.add_option("-h", "-?", "--help", action="help", help="Display this help page")
    parser.add_option("-n", "--line-numbers", action="store_true", dest="println", \
                       help="Print line-numbers of matches")
    parser.add_option("-f", "--filenames", action="store_true", dest="printfn", \
                       help="Print file names before matches")
    parser.add_option("-R", "--recursive", action="store_true", dest="recursive", \
                       help="Recursively process directories in the file list")
    parser.add_option("-v", "--version", action="version", \
                       help="Show author and version information and exit.")
    parser.add_option("-t", "--time", action="store_true", dest="time", \
                       help="Print out the processing time at the end of script run")

    # get options and arguments from argv
    (options, args) = parser.parse_args()

    # print usage information if no or too less arguments are supplied
    if len(args) < 2:
        parser.print_help()
        exit(0) # and quit

    pattern = args[0] # first argument is the regex pattern
    reg = re.compile(pattern) # precompile the pattern (more efficient)
    files = args[1:] # all other arguments are filenames

    # Everything's set up, so start working
    grepy(files, reg, options)

    if options.time:
        end_time = time.clock()
        print "Script run took " + str(end_time - start_time) + "s."

# Taken from:
# http://stackoverflow.com/questions/898669/how-can-i-detect-if-a-file-is-binary-non-text-in-python/3002505#3002505
def is_binary(filename):
    """Return true if the given filename is binary.
    @raise EnvironmentError: if the file does not exist or cannot be accessed.
    @attention: found @ http://bytes.com/topic/python/answers/21222-determine-file-type-binary-text on 6/08/2010
    @author: Trent Mick <TrentM@ActiveState.com>
    @author: Jorge Orpinel <jorge@orpinel.com>"""
    fin = open(filename, 'rb')
    try:
        CHUNKSIZE = 1024
        while 1:
            chunk = fin.read(CHUNKSIZE)
            if '\0' in chunk: # found null byte
                return True
            if len(chunk) < CHUNKSIZE:
                break # done
    # A-wooo! Mira, python no necesita el "except:". Achis... Que listo es.
    finally:
        fin.close()

    return False

def grepy(files, reg, options):
    # iterate over the filenames
    for filename in files:
        try:
            if is_binary(filename):
                print filename + " is a binary file. Skipping file."
            if os.path.isdir(filename):
                if options.recursive:
                    # generate a list of subfiles, joining the current directory path and its sub-entries
                    subfiles = [os.path.join(filename, entry) for entry in os.listdir(filename)]
                    # recurse over the files of the directory
                    grepy(subfiles, reg, options)
                # ...skip the directory, either because we are done recursing,
                # or we are not working recursive at all
                continue
            # file handles implement context manager for exceptions and stuff
            # see session 2 slide 21 (on with statements)
            with open(filename) as infile:
                # get all the lines. Yes, ALL the lines. Might be more convenient
                # to read lines one by one, but the former way allows us to enumerate
                # lines in advance
                lines = infile.readlines()
                # we want the line numbers too, see session 3 slide 29
                for linenumber, line in enumerate(lines):
                    # check if the line matches the pattern 
                    match = reg.search(line)
                    if match:
                        prepend = ""
                        if options.printfn:
                            prepend = filename + ":"
                        if options.println:
                            prepend = prepend + str(linenumber + 1) + ":"
                        if options.color:
                            # wrap some magic line chars for green color around the matched pattern see also:
                            # http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
                            print prepend + re.sub(match.group(0), "\033[92m" + match.group(0) + "\033[0m", line.rstrip())
                        else:
                            # always strip away line breaks at the end of lines
                            print prepend + line.rstrip()
                # done with the line
            # done with the the file
        # If something goes wrong with a file, simply skip it
        # and print an error
        except IOError:
            print filename + ": Error opening file. Skipping file."

if __name__ == '__main__': main()
