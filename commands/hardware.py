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
from util.spec import *
from util.config import config
from util.log import log
from util.softlayer.service import *
from util.softlayer.objects.hardware import *

def _get_hardware(hardware_spec, mask=None):
    """Generator returning all hardware matching hardware_spec"""
    account_service = get_account_service()
    account_service.set_object_mask(None)
    log.debug("fetching all hardware with %s" % (hardware_spec))
    for hardware in filter(hardware_spec, account_service.getHardware()):
        log.debug("fetching hardware server %d" % (hardware['id']))
        hardware_service = get_hardware_server_service(hardware['id'])
        hardware_service.set_object_mask(mask)
        hardware = hardware_service.getObject()
        pp(hardware)
        yield SoftLayerHardwareServer(hardware)

def _get_hardware_object_mask(properties):
    """Return an object mask for the given list of propeties"""
    default_mask = {'datacenter': {}, 'hardwareStatus': {}} 
    object_mask = default_mask
    for prop in properties:
        log.debug("getting hardware object mask for %s" % (prop))
        if prop in ['processor', 'proc', 'cpu', 'cpus']:
            object_mask['processors'] = {}
        elif prop in ['drives', 'disks', 'disk']:
            object_mask['hardDrives'] = {}
        elif prop in ['memory', 'mem']:
            object_mask['memory'] = {}
        elif prop in ['raid']:
            object_mask['raidControllers'] = {}
        elif prop in ['nic', 'nics']:
            object_mask['networkComponents'] = {'primarySubnet': {'networkVlan': {}}}
        elif prop in ['pwr', 'powersupply']:
            object_mask['powerSupply'] = {}
        elif prop in ['mobo', 'motherboard']:
            object_mask['motherboard'] = {}
        else:
            print_error("Unknown hardware property: %s" % (prop))
    log.debug("hardware object mask: %s" % (object_mask))
    return object_mask

def show(args):
    """usage: slapi hardware show [options] [<hardware_spec>]

    options:
        -p PROPERTIES
        -v, --verbose
        -F, --format
        -h, --help

    properties:
        cpu     show CPU infomration
        disk    show DISK information
        mem     show MEMORY information
        raid    show RAID CONTROLLER information
        nic     show NETWORK CARDS information
        pwr     show POWER SUPPLY information
        mobo    show MOTHERBOARD information
    """

    # Parse Arguments
    hardware_spec = parse_hardware_spec(args)
    properties = args['-p'].split(',') if args['-p'] else []

    # Generate Hardware Object Mask
    object_mask = _get_hardware_object_mask(properties) 

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

    object_mask = {'activeTransactions': {},
                    'lastTransaction': {
                        'transactionStatus': {},
                        'transactionGroup': {}}}

    # Parse Arguments
    hardware_spec = parse_hardware_spec(args)
    for hardware in _get_hardware(hardware_spec, object_mask):
        print hardware.format()
