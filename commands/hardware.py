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
        yield hardware

def _format_hardware(hardware, mask=None, color=True):
    default_mask = {'id': {},
            'hostname': {},
            'fullyQualifiedDomainName': 'fqdn',
            'primaryIpAddress': 'Public IP',
            'privateIpAddress': 'Private IP'}
    merged_mask = merge_dict(default_mask, mask) if mask else default_mask
    return format_object(hardware, merged_mask, color=color)

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
    object_mask = {'hardware': {
                        'lastTransaction': {
                            'transactionStatus': {}, 
                            'transactionGroup': {}}}}

    format_mask = {'lastTransaction': {
                        'createDate': {}, 
                        'modifyDate':{},
                        'transactionStatus': {
                            'friendlyName': 'Name'
                        },
                        'transactionGroup': {
                            'averageTimeToComplete': {},
                            'name': 'Name'
                        }
                  }}

    # Parse Arguments
    hardware_spec = parse_hardware_spec(args)

    # Show Hardware
    for hardware in _get_hardware(hardware_spec, object_mask):
        print _format_hardware(hardware, format_mask)

def transactions(args):
    """usage: slapi [options] hardware transactions [<hardware_spec>]

    options:
        -v, --verbose
        -F, --format
        -h, --help
    """

    def _format_transactions(hardware, fmt=None, color=True):
        hardware_id = hardware['id']
        hardware_hostname = hardware['fullyQualifiedDomainName']
        hardware_transactions = hardware['activeTransactions']
        if fmt == 'json':
            return json.dumps({'id': hardware_id,
                            'hostname': hardware_fqdn,
                            'transactions': hardware_active_transactions})
        else:
            output = ""
            output += output_attr('Id', hardware_id, ljust=25) + "\n"
            output += output_attr('Hostname', hardware_hostname, ljust=25) + "\n"
            output += output_attr('Active Transactions', '', ljust=25) + "\n"
            for transaction in hardware_transactions:
                output += output_attr("Transaction: %s" % (transaction))
            return output

    # Parse Arguments
    hardware_spec = parse_hardware_spec(args)
    mask = {'hardware': {'activeTransactions': {}}}
    for hardware in _get_hardware(hardware_spec, mask):
        print _format_transactions(hardware)
        #hardware_server_service = get_hardware_server_service(hardware['id'])
        #print hardware_service.getActiveTransactions()
