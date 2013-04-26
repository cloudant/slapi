"""
Usage: slapi datacenter <command> [<args>...]

Commands:
    datacenter show         Show datacenters
"""
from util.config import config
from util.log import log
from util.spec import parse_location_spec
from util.softlayer.service import get_datacenters
from util.softlayer.service import build_datacenter_object_mask


def show(args):
    """Show datacenters

    Usage: slapi datacenter show [options] [<location_spec>]

    Options:
        -F, --format FORMAT
        -h, --help
    """
    # Parse network_spec
    location_spec = parse_location_spec(args['<location_spec>'])
    object_mask = build_datacenter_object_mask()

    for datacenter in get_datacenters(location_spec, object_mask):
        print datacenter.format()
