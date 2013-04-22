import json
import yaml
import sys
import colorama as COLORS
from copy import deepcopy

from pprint import pprint as pp

COLOR_LABEL = COLORS.Fore.CYAN + COLORS.Style.BRIGHT
COLOR_RESET = COLORS.Style.RESET_ALL

def confirm(question, default="no"):
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}

    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

def format_object(obj, level=0, color=True):
    output = ""
    if isinstance(obj, dict):
        output += _format_dict_object(obj, level=level, color=color) 
    elif isinstance(obj, list):
        output += _format_list_object(obj, level=level, color=color) 
    else:
        output += str(obj) + "\n"
    return output

def _format_dict_object(obj, level, color):
    output = "\n"
    ljust = max(map(lambda k: len(k) if k else 0, obj.keys())) + 4
    # calculate indent level
    output_indent = " "*(level*2)
    # iterate all items in the dict 
    for key, val in obj.iteritems():
        # use the object key as the label
        output_key = _format_label(key, ljust, color)
        # format the item value 
        output_value = format_object(val, level+1, color=color)
        output += output_indent + output_key + output_value
    return output

def _format_list_object(obj, level, color):
    output = ""
    if len(obj) > 0:
        for item in obj:
            output += format_object(item, level, color=color)
    else:
        output += format_object("None", level, color=color) 
    return output

def _format_label(label, ljust, color):
    label = label[0].upper() + label[1:]
    if color:
        ljust += 12 # offset for color escapes
        output_label = "%s%s%s:" % (COLOR_LABEL, label, COLOR_RESET)
    else:
        output_label = "%s:" % (label)
    return output_label.ljust(ljust)

def merge_dict(a, b): 
    if not isinstance(b, dict):
        return b
    result = deepcopy(a)
    for k, v in b.iteritems():
        if k in result and isinstance(result[k], dict):
            result[k] = merge_dict(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result

def configure_colors():
    COLORS.init()

def colored(message, fg=None, bg=None, style=None):
    color_fg = getattr(COLORS.Fore, fg.upper()) if fg else COLORS.Fore.RESET
    color_bg = getattr(COLORS.Back, bg.upper()) if bg else COLORS.Back.RESET
    color_style = getattr(COLORS.Style, style.upper()) if style else COLORS.Style.NORMAL
    return color_fg + color_bg + color_style + message + COLORS.Style.RESET_ALL

def warning(message, label="WARNING: "):
    return colored(label + message, fg='yellow', style='bright')

def error(message, label="ERROR: "):
    return colored(label + message, fg='red', style='bright')

def critical(message, label=""):
    return colored(label + message, fg='white', bg='red', style='bright')
