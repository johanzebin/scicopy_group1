#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
grepy implements some core functionality of the UNIX grep command.
@author: Johannes Keyser (jkeyser@uos.de)
"""

from optparse import OptionParser
import os
import sys
import re

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

if __name__ == "__main__":
    GREPY_PARSER    = _setup_grepy_parser()
    (OPTIONS, ARGS) = GREPY_PARSER.parse_args()
    # reject if either PATTERN or FILE is missing
    if len(ARGS) < 2:
        GREPY_PARSER.print_help()
        sys.exit(2)
    # pick out PATTERN, FILE(s) and directories, while ignoring (symbolic) links
    PATTERN  = ARGS[0]
    NOLINKS  = [arg for arg in ARGS[1:] if not os.path.islink(arg)]
    ARGFILES = [arg for arg in NOLINKS  if os.path.isfile(arg)]
    ARGDIRS  = [arg for arg in NOLINKS  if os.path.isdir(arg)]
    # generate a list of all files to search for PATTERN, while ignoring links
    FILEPATHS = ARGFILES # start with explicitely stated files
    if OPTIONS.traverse_recursively:
        for folder in ARGDIRS:
            for path, _, files in os.walk(folder, topdown=False):
                # extend file list with all non-link files
                FILEPATHS.extend([os.path.join(path, fl) for fl in files \
                                  if not os.path.islink(fl)])
    #print FILEPATHS
    # find occurences of PATTERN in all files in the list & print them
    RE_PATTERN = re.compile(PATTERN)
    for flpth in FILEPATHS:
        with open(flpth, 'r') as fl:
            for lnum, line in enumerate(fl, start=1):
                MATCHES = RE_PATTERN.findall(line)
                if not MATCHES:
                    continue
                #print MATCHES
                # prepare output format according to options
                OUT_STR = ""
                if OPTIONS.print_filenames:
                    pass
                if OPTIONS.print_line_number:
                    pass
