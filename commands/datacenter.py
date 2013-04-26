"""
Usage: slapi datacenter <command> [<args>...]

Commands:
    datacenter show         Show datacenters
"""
from util.spec import parse_location_spec
from util.config import config
from util.log import log
from util.softlayer.service import get_objects, get_service
from util.softlayer.objects.core import SoftLayerLocation


def _get_datacenters(location_spec, mask):
    """Generator returning datacenters matching location_spec"""
    datacenter_service = get_service('SoftLayer_Location_Datacenter')
    datacenter_service.set_object_mask(mask)
    for obj in filter(location_spec, datacenter_service.getViewableDatacenters()):
        yield SoftLayerLocation(obj)


def _get_datacenter_object_mask():
    object_mask = dict()
    object_mask['locationAddress'] = dict()
    #object_mask['frontendHardwareRouters'] = dict()
    #object_mask['backendHardwareRouters'] = dict()
    return object_mask


def show(args):
    """Show datacenter

    Usage: slapi datacenter show [options] [<location_spec>]

    Options:
        -F, --format FORMAT
        -h, --help
    """
    # Parse network_spec
    location_spec = parse_location_spec(args['<location_spec>'])
    object_mask = _get_datacenter_object_mask()

    for datacenter in _get_datacenters(location_spec, object_mask):
        print datacenter.format()
