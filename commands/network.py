"""
Usage: slapi network <command> [<args>...]

Commands:
    network subnets         Show network subnets
    network vlans           Show network subnets
"""
from util.spec import parse_subnet_spec
from util.spec import parse_vlan_spec
from util.config import config
from util.log import log
from util.softlayer.service import get_vlans
from util.softlayer.service import get_private_vlans, get_public_vlans
from util.softlayer.service import get_subnets
from util.softlayer.service import build_vlan_object_mask
from util.softlayer.service import build_subnet_object_mask


def subnets(args):
    """Show subnets

    Usage: slapi network subnets [options] [<vlan_spec>]

    Options:
        -F, --format FORMAT
        -h, --help
    """
    # Parse network_spec
    subnet_spec = parse_subnet_spec(args)
    object_mask = build_subnet_object_mask()

    for subnet in get_subnets(subnet_spec, object_mask):
        print subnet.format()


def vlans(args):
    """Show VLANs

    Usage: slapi network vlans [options] [<vlan_spec>]

    Options:
        -p, --public                Filter for ublic VLANs
        -x, --private               Filter for private VLANs
        -l, --location LOCATION     Filter VLANs in LOCATION (e.g. dal05)
        -s, --subnets               Show subnets attached to VLANS
        -F, --format FORMAT
        -h, --help
    """
    # Parse vlan spec
    vlan_spec = parse_vlan_spec(args['<vlan_spec>'])
    object_mask = build_vlan_object_mask(
        include_subnets=(args['--subnets'] is True))

    # Parse args
    if args['--public']:
        # get public vlans
        vlanlist = get_public_vlans(vlan_spec, object_mask)
    elif args['--private']:
        # get private vlans
        vlanlist = get_private_vlans(vlan_spec, object_mask)
    else:
        # get all vlans
        vlanlist = get_vlans(vlan_spec, object_mask)

    # Filter vlans by location of primary router
    if args['--location'] is not None:
        filter_func = lambda vlan: vlan.primary_router.datacenter.name == args['--location']
    else:
        filter_func = lambda vlan: True

    for vlan in filter(filter_func, vlanlist):
        print vlan.format()
