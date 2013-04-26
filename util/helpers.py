import sys
import colorama as COLORS


def confirm(question, default="no"):
    """Prompt for user confirmation (yes or no)"""
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}

    if default is None:
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
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def configure_colors():
    """Initialize ANSI Colors"""
    COLORS.init()


def colored(message, fg=None, bg=None, style=None):
    """Return a message colored with ANSI color codes"""
    if fg:
        color_fg = getattr(COLORS.Fore, fg.upper())
    else:
        color_fg = COLORS.Fore.RESET

    if bg:
        color_bg = getattr(COLORS.Back, bg.upper())
    else:
        color_bg = COLORS.Back.RESET

    if style:
        color_style = getattr(COLORS.Style, style.upper())
    else:
        color_style = COLORS.Style.NORMAL

    return color_fg + color_bg + color_style + message + COLORS.Style.RESET_ALL


def warning(message, label="WARNING: "):
    """Return a colored WARNING message"""
    return colored(label + message, fg='yellow', style='bright')


def error(message, label="ERROR: "):
    """Return a colored ERROR message"""
    return colored(label + message, fg='red', style='bright')


def critical(message, label=""):
    """Return a colored CRITICAL message"""
    return colored(label + message, fg='white', bg='red', style='bright')
