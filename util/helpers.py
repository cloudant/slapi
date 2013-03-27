import json
import yaml
import sys
import colorama as COLORS
from copy import deepcopy

from pprint import pprint as pp

COLOR_LABEL = COLORS.Fore.CYAN + COLORS.Style.BRIGHT
COLOR_RESET = COLORS.Style.RESET_ALL


def format_object(obj, mask=None, level=0, color=True):
    output = ""
    if isinstance(obj, dict):
        output += _format_dict_object(obj, mask, level=level, color=color)
    elif isinstance(obj, list):
        output += _format_list_object(obj, mask, level=level, color=color)
    else:
        output += str(obj) + "\n"
    return output

def _format_dict_object(obj, mask, level, color):
    output = "\n"
    labels = obj.keys() + filter(lambda v: isinstance(v, str), mask.values())
    ljust = max(map(lambda k: len(k), labels)) + 2
    # calculate indent level
    output_indent = " "*(level*2)
    # iterate all items in the dict 
    for key, val in obj.iteritems():
        # if the key is in the mask
        if key in mask:
            # if the mask value is a string
            if isinstance(mask[key], str):
                # use the value as the label
                output_key = _format_label(mask[key], ljust, color)
            else:
                # use the object key as the label
                output_key = _format_label(key, ljust, color)
            print output_key, ljust
            # format the item value 
            output_value = format_object(val, mask[key], level+1, color=color)
            output += output_indent + output_key + output_value
        else:
            # dont print the item
            continue
    return output

def _format_label(label, ljust, color):
    label = label[0].upper() + label[1:]
    if color:
        ljust += 7 # offset for color escapes
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

def print_usage_and_exit(doc):
    print doc
    sys.exit(1)

def print_error(message, exit=False):
    print COLORS.Fore.RED + COLORS.Style.BRIGHT + "Error: "+ message
    if exit:
        sys.exit(1)

if __name__ == "__main__":
    obj = {'foo': {'bar': 'baz'}, 'what': "derp"}
    print format_object(obj)
