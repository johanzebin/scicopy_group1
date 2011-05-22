#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
grepy implements some core functionality of the *nix grep command.
@author: Johannes Keyser (jkeyser@uos.de)
"""

from optparse import OptionParser
import os
import sys
import re
import string

def _color_string(text="", color_str="yellow"):
    """
    Adds ANSI escape codes to the string 'text' according to a few color
    names handed over as strings in 'color_str'. When printed, the modified
    text should appear colored (if the used terminal emulator allows it).
    Look at http://en.wikipedia.org/wiki/ANSI_escape_code for more information.
    """
    _colormap = {'black':30, 'blue':34, 'yellow':33, 'cyan':36, 'green':32,
                 'magenta':35, 'red':31, 'white':37}
    if color_str not in _colormap.keys():
        err_str = "No such color option! Possible values: %s" % \
            _colormap.keys().__str__()
        raise ValueError(err_str)
    return "\033[0;%dm%s\033[0m" % (_colormap.get(color_str), text)

def _setup_grepy_parser():
    """
    Sets up an optparse-command line parser specific for grepy.
    """
    usage = "%prog [OPTIONS] PATTERN FILE [FILE...]"
    versn = "%prog version 1.0 jk"
    descr = "%prog searches the named input FILEs for lines containing"\
           +" a match to the given PATTERN and prints them. Links are ignored!"
    parser = OptionParser(usage=usage, version=versn, description=descr)
    parser.add_option("-c", "--color", dest="colorize_output",
                      default=False, action="store_true",
                      help="Highlight the matching string in color.")
    parser.add_option("-n", "--line-number", dest="print_line_number",
                      default=False, action="store_true",
                      help="Prefix output line with the line number.")
    parser.add_option("-f", "--filenames", dest="print_filenames",
                      default=False, action="store_true",
                      help="Print filenames before occurence of PATTERN.")
    parser.add_option("-R", "--recursive", dest="traverse_recursively",
                      default=False, action="store_true",
                      help="Read all files under each directory, recursively.")
    return parser

def _create_file_paths(arglist, recursively=False):
    """
    Generates the complete list of files based on the argument list,
    optionally traversing the directory tree recursively.
    Symbolic links are silently ignored, binary files are NOT sorted out.
    """
    nolinks  = [arg for arg in arglist if not os.path.islink(arg)]
    argfiles = [arg for arg in nolinks if os.path.isfile(arg)]
    argdirs  = [arg for arg in nolinks if os.path.isdir(arg)]
    # generate a list of all files, while ignoring links
    filepaths = argfiles # start with explicitely stated files (dirs)
    if recursively:
        for folder in argdirs:
            for path, _, files in os.walk(folder, topdown=False):
                # extend file list with all non-link files
                filepaths.extend([os.path.join(path, fil) for fil in files \
                                  if not os.path.islink(fil)])
    return filepaths

def grep_core_function(pattern, filepaths, options):
    """
    Finds occurences of 'pattern' in all files in 'filepaths',
    and prints them to stdout according to 'options'.
    Tries to silently ignore non-text files.
    """
    re_pattern = re.compile(pattern)
    for flpth in filepaths:
        with open(flpth, 'r') as fil:
            # naive detection of binary files: non-printing char in 1st "line"?
            if [ch for ch in fil.readline() if not ch in string.printable]:
                continue
            for lnum, line in enumerate(fil, start=1):
                m_obj = re_pattern.search(line)
                if not m_obj: # no match found: get next line!
                    continue
                match = m_obj.group()
                # prepare output format according to options
                out_str = ""
                if options.print_filenames:
                    out_str += "%s:" % flpth
                if options.print_line_number:
                    out_str += "%d:" % lnum
                if options.colorize_output:
                    line = line.replace(match, _color_string(match, "red"))
                out_str += line.rstrip()
                print out_str

if __name__ == "__main__":
    GREPY_PARSER    = _setup_grepy_parser()
    (OPTIONS, ARGS) = GREPY_PARSER.parse_args()
    # reject if either PATTERN or FILE is missing
    if len(ARGS) < 2:
        GREPY_PARSER.print_help()
        sys.exit(2)
    # get FILE(s) while ignoring symbolic links
    FILEPATHS = _create_file_paths(ARGS[1:], OPTIONS.traverse_recursively)
    # in every file, search for PATTERN in each line & print it
    grep_core_function(ARGS[0], FILEPATHS, OPTIONS)
