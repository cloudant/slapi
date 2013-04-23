"""usage: slapi [options] network <command> [<args>...]

options:
    -v, --verbose
    -h, --help

commands:
    network subnets         Show network subnets
    network vlans           Show network subnets
"""
from util.spec import parse_subnet_spec
from util.spec import parse_vlan_spec
from util.config import config
from util.log import log
from util.softlayer.service import get_objects, get_service
from util.softlayer.objects.network import SoftLayerNetworkVLAN
from util.softlayer.objects.network import SoftLayerNetworkSubnet
from pprint import pprint as pp


def _get_subnets(subnet_spec, mask):
    """Generator returning network subnets matching subnet_spec"""
    for obj in get_objects('SoftLayer_Network_Subnet', 'getSubnets', subnet_spec, mask):
        yield SoftLayerNetworkSubnet(obj)


def _get_vlans(vlan_spec, mask):
    """Generator returning primary network vlans matching subnet_spec"""
    for obj in get_objects('SoftLayer_Network_Vlan', 'getNetworkVlans', vlan_spec, mask):
        yield SoftLayerNetworkVLAN(obj)

def _get_public_vlans(vlan_spec, mask):
    """Generator returning public network vlans matching vlan_spec"""
    for obj in get_objects('SoftLayer_Network_Vlan', 'getAvailablePublicNetworkVlans', vlan_spec, mask):
        yield SoftLayerNetworkVLAN(obj)

def _get_private_vlans(vlan_spec, mask):
    """Generator returning private network vlans matching vlan_spec"""
    for obj in get_objects('SoftLayer_Network_Vlan', 'getAvailablePublicNetworkVlans', vlan_spec, mask):
        yield SoftLayerNetworkVLAN(obj)


def get_subnet_object_mask(**kwargs):
    object_mask = dict()
    object_mask['networkVlan'] = {}
    return object_mask


def get_vlan_object_mask(**kwargs):
    object_mask = dict()
    object_mask['primarySubnet'] = dict()
    object_mask['additionalPrimarySubnets'] = dict()
    object_mask['secondarySubnets'] = dict()
    object_mask['primaryRouter'] = dict()
    object_mask['primaryRouter']['datacenter'] = dict()
    object_mask['secondaryRouter'] = dict()
    object_mask['secondaryRouter']['datacenter'] = dict()
    return object_mask


def subnets(args):
    """usage: slapi network subnets [options] [<vlan_spec>]

    options:
        -F, --format FORMAT
        -h, --help

    """
    # Parse network_spec
    subnet_spec = parse_subnet_spec(args)
    object_mask = get_subnet_object_mask() 

    for subnet in _get_subnets(subnet_spec, object_mask):
        print subnet.format()

def vlans(args):
    """usage: slapi network vlans [options] [<vlan_spec>]

    options:
        -p, --public
        -x, --private
        -F, --format FORMAT
        -h, --help

    """
    # Parse vlan spec 
    vlan_spec = parse_vlan_spec(args['<vlan_spec>'])
    object_mask = get_vlan_object_mask()

    # Parse args
    if args['--public'] is not None:
        # get public vlans
        vlans = _get_public_vlans(vlan_spec, object_mask)
    elif args['--private'] is not None:
        # get private vlans
        vlans = _get_private_vlans(vlan_spec, object_mask)
    else:
        vlans = _get_vlans(vlan_spec, object_mask)

    for vlan in vlans: 
        print vlan.format()
