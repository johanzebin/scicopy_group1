#from optparse import OptionParser

def color_string(text="", color_str="yellow"):
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

if __name__ == "__main__":
    pass


