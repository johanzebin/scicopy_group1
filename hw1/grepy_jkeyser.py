#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
grepy implements some core functionality of the *nix grep command.
   @author: Johannes Keyser (jkeyser@uos.de)
@attention: SCICOPY homework 1
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

def is_textfile(filepath, checklength=10*1024, max_chunk=1024**2):
    """
    Attempts to detect non-text files based on the existence of 0-Bytes.
    To save time, at most 'checklength' many bytes of the file are checked;
    to search the whole file, pass a negative number (cf. file.read()).
    If 'checklength' is negative, at most 'max_chunk' bytes are read at a time
    until the entire file is read.
    """
    # ensure a sensible maximal amount of bytes to be read in one go
    if checklength > 0 and checklength < max_chunk:
        chunk_size = checklength
    else:
        chunk_size = max_chunk
    already_read_bytes = 0
    with open(filepath, 'rb') as fil:
        while True:
            chunk = fil.read(chunk_size)
            already_read_bytes += len(chunk)
            # assume non-text files don't contain 0-bytes
            if '\x00' in chunk:
                break
            # check only the wanted amount of bytes
            if checklength > 0 and already_read_bytes >= checklength:
                return True
            # if reached end of file, no 0-byte was found
            if not chunk:
                return True
    return False

def _setup_grepy_parser():
    """
    Sets up an optparse-command line parser specific for grepy.
    """
    usage  = "%prog [OPTIONS] PATTERN FILE [FILE...]"
    versn  = "%prog version 1.1 jk"
    descr  = "%prog searches the named input FILEs for lines containing "\
            +"a match to the given PATTERN and prints them. "\
            +"Links and non-readable files are ignored!"
    parser = OptionParser(usage=usage, version=versn, description=descr)
    # change conflict handler, so "-?" option can be added to "help" action
    parser.set_conflict_handler(handler="resolve")
    parser.add_option("-h", "-?", "--help", action="help",
                      help="show this help message and exit")
    parser.add_option("-c", "--color", dest="colorize_output",
                      default=False, action="store_true",
                      help="highlight the matching string in color")
    parser.add_option("-n", "--line-number", dest="print_line_number",
                      default=False, action="store_true",
                      help="prefix output line with the line number")
    parser.add_option("-f", "--filenames", dest="print_filenames",
                      default=False, action="store_true",
                      help="print filenames before occurence of PATTERN")
    parser.add_option("-R", "--recursive", dest="traverse_recursively",
                      default=False, action="store_true",
                      help="recursively read all files under each directory")
    parser.add_option("-b", "--binary", dest="ignore_binary_files",
                      default=True, action="store_false",
                      help="do not ignore binary files")
    return parser

def _create_file_paths(arglist, recursively=False, ignore_bins=True):
    """
    Generates the complete list of files based on 'arglist',
    optionally traversing the directory tree recursively.
    Symbolic links and non-readable files are silently ignored.
    Binary files may be included into list with 'ignore_bins'.
    """
    # filter out links and non-readable files
    nobogus  = [arg for arg in arglist if not os.path.islink(arg)\
                                          and os.access(arg, os.R_OK)]
    argfiles = [arg for arg in nobogus if os.path.isfile(arg)]
    argdirs  = [arg for arg in nobogus if os.path.isdir(arg)]
    # generate a list of all files, while ignoring links and non-readable files
    filepaths = argfiles # start with explicitely stated files (dirs)
    if recursively:
        for folder in argdirs:
            for path, _, files in os.walk(folder, topdown=False):
                # extend file list with all non-link files which are readable
                filepaths.extend([os.path.join(path, fil) for fil in files])
        # filter out links and non-readable files
        filepaths = [flpth for flpth in filepaths\
                    if not os.path.islink(flpth) and os.access(flpth, os.R_OK)]
    if ignore_bins:
        filepaths = [flpth for flpth in filepaths if is_textfile(flpth)]
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
            for line_num, line in enumerate(fil, start=1):
                match_obj = re_pattern.search(line)
                if not match_obj: # no match found: get next line!
                    continue
                match = match_obj.group() # get matched string
                # prepare output format according to options
                out_str = ""
                if options.print_filenames:
                    out_str += "%s:" % flpth
                if options.print_line_number:
                    out_str += "%d:" % line_num
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
    FILEPATHS = _create_file_paths(ARGS[1:], OPTIONS.traverse_recursively,
                                   OPTIONS.ignore_binary_files)
    # in every file, search for PATTERN in each line & print it
    grep_core_function(ARGS[0], FILEPATHS, OPTIONS)
