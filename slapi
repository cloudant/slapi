#!/usr/bin/env python
"""usage: slapi [options] <command> [<args>...]

options:
    -c, --config CONFIGFILE
    -v, --verbose
    -h, --help

The most commonly used slapi commands are:
    hardware        List, provision, or query hardware
    commands        List available commands
"""
import os
import sys
import re
import json
import inspect
import traceback
import docopt

from util.config import config, _load_config 
from util.log import log, configure_log
from util.helpers import *

#==============================================================================
# Constants
#==============================================================================
VERSION = '0.1.0'
MODULE_DIR = 'commands'

DEFAULT_LOGLEVEL = 'INFO'
DEFAULT_CONFIGFILE = "%s/.slapi.conf" % (os.path.expanduser("~"))

#==============================================================================
# Helpers 
#==============================================================================

def _get_root_directory():
    """Return slapi root directory"""
    return os.path.dirname(os.path.realpath(__file__))

def _get_installed_commands():
    """Generator returning all commands in MODULE_DIR"""
    for f in os.listdir(os.path.join(_get_root_directory(), MODULE_DIR)):
        if not f.startswith('.') and not f.startswith('_') and f.endswith('.py'):
            yield os.path.splitext(f)[0]

def _get_builtin_commands():
    yield None

def _load_command_module(name):
    """Import given command module"""
    try:
        module =  getattr(__import__('.'.join([MODULE_DIR, name])), name)
        log.debug("loaded module: %s" % ('.'.join([MODULE_DIR, name])))
        return module
    except ImportError:
       print_error(traceback.format_exc()) 
    return None

def _get_module_commands(module):
    """Generator returning all commands in the given module"""
    for func_name, value in inspect.getmembers(module):
        if not func_name.startswith('_'):
            yield func_name

def _handle_command(module, global_args):
    log.debug("_handle_command: %s" % (module.__name__))

    # Get command
    command = global_args['<command>']

    # Check if subcommand was given
    if len(global_args['<args>']) > 0:
        # Get subcommand
        subcommand = global_args['<args>'][0]
        if subcommand in list(_get_module_commands(module)):
            # Get subcommand function from module
            func = getattr(module, subcommand)

            # Parse subcommand arguments from module.func's docstring
            subcommand_argv = [command, subcommand] + global_args['<args>'][1:]
            subcommand_args = docopt.docopt(func.__doc__, argv=subcommand_argv)

            # Handle subcommand
            _handle_subcommand(module, func, subcommand_args)
        else:
            print_error("Unknown subcommand: %s" % (subcommand))
            print_usage_and_exit(module.__doc__)

    else:
        # If no subcommand was given, invoke the modules main function
        if hasattr(module, 'main'):
            func = getattr(module, 'main')

            # Parse subcommand arguments from module.func's docstring
            subcommand_argv = [command] + global_args['<args>']
            subcommand_args = docopt.docopt(func.__doc__, argv=subcommand_argv)

            # Handle subcommand
            _handle_subcommand(module, func, subcommand_args)
        else:
            # If no main function is defined, just print the docstring
            print_usage_and_exit(module.__doc__)

def _handle_subcommand(module, func, subcommand_args):
    log.debug("_handle_subcommand: %s.%s" % (module.__name__, func.__name__))

    # Invoke subcommand
    func(subcommand_args)

if __name__ == "__main__":
    # Configure Colors
    configure_colors()

    # Parse Command Arguments
    global_args = docopt.docopt(__doc__, version=VERSION, options_first=True)

    loglevel = 'DEBUG' if global_args['--verbose'] else DEFAULT_LOGLEVEL 
    configfile = global_args['--config'] if global_args['--config'] else DEFAULT_CONFIGFILE

    # Load Configuration
    _load_config(configfile)

    # Configure Log
    configure_log(log, loglevel)

    # Handle Command
    command = global_args['<command>']
    if command in list(_get_builtin_commands()):
        # TODO: Built in commands
        pass
    if command in list(_get_installed_commands()):
        # Load command module
        command_module = _load_command_module(command)
        _handle_command(command_module, global_args)
    else:
        print_error("Unknown command: %s" % (command))
        print_usage_and_exit(__doc__)
