import re

def grepy(pattern, file):
    reguexp = re.compile(pattern)
    for text in file:
        match = reguexp.search(text)
        if match != None:
            print match.pattern

# command line should work as follows: 
#
# grepy PATTERN FILE [FILE] [Options]
# (searches for PATTERN in FILE[S])
# e.g.: grepy py*hon *.py

# command line switches for grepy:
# -c, --color
# Highlight the matching string in color.
# -h , -?, --help
# Print a help message. The same message should be printed if no arguments were given at all.
# -n, --line-number
# Prefix each output line with the line number in its input file.
# -f, --filenames
# Print filenames before occurence of PATTERN.
# -R, --recursive
# Read all files under each directory, recursively.
# --version
# Prints author details and version number.


# os.system(command)
# Execute the command (a string) in a subshell. This is implemented by calling the Standard C function system(), and has the same limitations. 
# Changes to sys.stdin, etc. are not reflected in the environment of the executed command.
# On Unix, the return value is the exit status of the process encoded in the format specified for wait(). 
# Note that POSIX does not specify the meaning of the return value of the C system() function, so the return value of the Python function is system-dependent.
# On Windows, the return value is that returned by the system shell after running command, 
# given by the Windows environment variable COMSPEC: on command.com systems (Windows 95, 98 and ME) this is always 0; 
# on cmd.exe systems (Windows NT, 2000 and XP) this is the exit status of the command run; on systems using a non-native shell, consult your shell documentation.
#
# The subprocess module provides more powerful facilities for spawning new processes and retrieving their results; 
# using that module is preferable to using this function. See the Replacing Older Functions with the subprocess Module section in the subprocess documentation for some helpful recipes.