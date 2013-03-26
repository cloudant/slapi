import json
import yaml
import sys
import colorama as COLORS

from pprint import pprint as pp

COLOR_CYAN = COLORS.Fore.CYAN + COLORS.Style.BRIGHT
COLOR_RESET = COLORS.Style.RESET_ALL

def configure_colors():
    COLORS.init()

def output_attr(label, attr, color=True, ljust=12):
    output_label = "%s:" % (label)
    output = COLOR_CYAN + output_label.ljust(ljust) + COLOR_RESET + "%s" % (attr)
    return output

def print_usage_and_exit(doc):
    print doc
    sys.exit(1)

def print_error(message, exit=False):
    print COLORS.Fore.RED + COLORS.Style.BRIGHT + "Error: "+ message
    if exit:
        sys.exit(1)
