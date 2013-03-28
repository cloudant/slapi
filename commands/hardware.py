"""usage: slapi [options] hardware <command> [<args>...]

options:
    -v, --verbose
    -h, --help

commands:
    hardware show               Show hardware
    hardware transactions       List pending hardware transactions
    hardware reboot             Reboot hardware
"""
from util.helpers import *
from util.softlayer import *
from util.spec import *
from util.config import config

def _get_hardware(hardware_spec, mask=None):
    """Generator returning all hardware matching hardware_spec"""
    account_service = get_account_service()
    account_service.set_object_mask(mask)
    for hardware in filter(hardware_spec, account_service.getHardware()):
        yield SoftLayerHardwareServer(hardware)

def _get_hardware_object_mask(type):
    pass

def show(args):
    """usage: slapi [options] hardware show [<hardware_spec>]

    options:
        -a, --attributes
        -v, --verbose
        -F, --format
        -h, --help
    """
    # Parse Arguments
    hardware_spec = parse_hardware_spec(args)

    object_mask = {'hardware': {'datacenter': {}}} 

    # Show Hardware
    for hardware in _get_hardware(hardware_spec, object_mask):
        print hardware.format()

def transactions(args):
    """usage: slapi [options] hardware transactions [<hardware_spec>]

    options:
        -v, --verbose
        -F, --format
        -h, --help
    """

    object_mask = {'hardware': {
                        'activeTransactions': {},
                        'lastTransaction': {
                            'transactionStatus': {}, 
                            'transactionGroup': {}}}}

    # Parse Arguments
    hardware_spec = parse_hardware_spec(args)
    for hardware in _get_hardware(hardware_spec, object_mask):
        print hardware.format()
