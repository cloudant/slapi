"""usage: slapi [options] network <command> [<args>...]

options:
    -v, --verbose
    -h, --help

commands:
    network subnets         Show network subnets
    network vlans           Show network subnets
"""


from pprint import pprint as pp

from util.spec import parse_subnet_spec
from util.spec import parse_vlan_spec
from util.config import config
from util.log import log
from util.softlayer.service import get_vlans, get_private_vlans, get_public_vlans
from util.softlayer.service import get_subnets
from util.softlayer.service import build_vlan_object_mask
from util.softlayer.service import build_subnet_object_mask



def subnets(args):
    """usage: slapi network subnets [options] [<vlan_spec>]

    options:
        -F, --format FORMAT
        -h, --help

    """
    # Parse network_spec
    subnet_spec = parse_subnet_spec(args)
    object_mask = build_subnet_object_mask() 

    for subnet in get_subnets(subnet_spec, object_mask):
        print subnet.format()


def vlans(args):
    """usage: slapi network vlans [options] [<vlan_spec>]

    options:
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
            include_subnets=(args['--subnets'] == True))

    # Parse args
    if args['--public']:
        # get public vlans
        vlans = get_public_vlans(vlan_spec, object_mask)
    elif args['--private']:
        # get private vlans
        vlans = get_private_vlans(vlan_spec, object_mask)
    else:
        # get all vlans
        vlans = get_vlans(vlan_spec, object_mask)

    # Filter vlans by location of primary router
    if args['--location'] is not None:
        filter_func = lambda vlan: vlan.primary_router.datacenter.name == args['--location']
    else:
        filter_func = lambda vlan: True

    for vlan in filter(filter_func, vlans):
        print vlan.format()
