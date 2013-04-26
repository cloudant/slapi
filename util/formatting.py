import colorama as COLORS

COLOR_LABEL = COLORS.Fore.CYAN + COLORS.Style.BRIGHT
COLOR_RESET = COLORS.Style.RESET_ALL


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
        ljust += 12  # offset for color escapes
        output_label = "%s%s%s:" % (COLOR_LABEL, label, COLOR_RESET)
    else:
        output_label = "%s:" % (label)
    return output_label.ljust(ljust)
