"""usage: slapi [options] hardware <command> [<args>...]

options:
    -v, --verbose
    -h, --help

commands:
    hardware show               Show hardware information
    hardware transactions       List pending hardware transactions
    hardware osreload           Reload operating system
"""
import sys

from util.helpers import error, warning, critical, colored, confirm
from util.spec import parse_hardware_spec
from util.config import config
from util.log import log
from util.softlayer.service import get_service, get_objects
from util.softlayer.objects.hardware import SoftLayerHardwareServer


def _get_hardware_service(object_id=None):
    return get_service('SoftLayer_Hardware_Server', object_id)


def _get_hardware(hardware_spec, mask):
    """Generator returning all hardware matching hardware_spec"""
    for obj in get_objects('SoftLayer_Hardware_Server', 'getHardware', hardware_spec, mask):
        yield SoftLayerHardwareServer(obj)


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
            print error("Unknown hardware property: %s" % (prop))
            sys.exit(1)
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
    """usage: slapi hardware transactions [options] [<hardware_spec>]

    options:
        -a, --active
    """
    # Parse Arguments
    hardware_spec = parse_hardware_spec(args)

    # Hardware Mmask should include transaction info
    object_mask = {'activeTransactions': {},
                    'lastTransaction': {
                        'transactionStatus': {},
                        'transactionGroup': {}}}

    # Output info
    for hardware in _get_hardware(hardware_spec, object_mask):
        print hardware.format()


def osreload(args):
    """usage: slapi hardware osreload [options] [<hardware_spec>]

    options:
        -c, --confirm TOKEN
    """
    # Parse Arguments
    hardware_spec = parse_hardware_spec(args)

    # Get Hardware
    hardware = list(_get_hardware(hardware_spec, None))
    if not hardware:
        print warning("No objects found matching spec: %s." % args['<hardware_spec>'])
        return

    # Refuse hardware_specs that match more then one host
    if len(hardware) > 1:
        print error("More then one object matching spec: %s. Refusing to continue." % args['<hardware_spec>'])
        sys.exit(1)

    # Get server object
    server = hardware[0]

    # Get hardware service
    service = _get_hardware_service(server['id'])

    confirmation_token = args['--confirm']

    # Check for confirmation_token option
    if confirmation_token is None:
        # Prompt for confirmation
        print critical("You are about to issue an OS reload on %s." % server.fqdn, label="WARNING: ")
        print critical("This will destroy all data on the device.", label="WARNING: ")
        if confirm(colored("Are you sure you want to continue?", fg='red', style='bright')):
            token = service.reloadCurrentOperatingSystemConfiguration()
            print "OS reload issued, confirm with token: %s" % (token)
            return

    else:
        # Prompt for confirmation
        print critical("You are about to confirm an OS reload on %s." % server.fqdn, label="WARNING: ")
        print critical("This will destroy all data on the device.", label="WARNING: ")
        print critical("This is your last chance to abort.", label="WARNING: ")
        if confirm(colored("Are you sure you want to continue?", fg='red', style='bright')):
            service.reloadCurrentOperatingSystemConfiguration(token=confirmation_token)
            print "OS Reload Started on %s" % (server.fqdn)
            return
