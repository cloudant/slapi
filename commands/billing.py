"""
Usage: slapi billing <command> [<args>...]

Commands:
    billing quotes          Show quotes
    billing orders          Show orders
    billing orderquote      Place an order
"""
import sys

from pprint import pprint as pp

from util.helpers import error, warning, critical, colored, confirm
from util.spec import parse_quote_spec, parse_order_spec
from util.spec import parse_vlan_spec
from util.config import config
from util.log import log
from util.softlayer.service import get_quotes, get_orders, get_service
from util.softlayer.service import get_public_vlans, get_private_vlans
from util.softlayer.service import build_vlan_object_mask
from util.softlayer.objects.billing import SoftLayerContainerProductOrder


def _verify_order(quote_id, order_container):
    order_service = get_service('SoftLayer_Billing_Order_Quote', quote_id)
    log.debug("verifying order for quote %d" % (quote_id))
    verified_order_container = SoftLayerContainerProductOrder(
            order_service.verifyOrder(order_container._data))
    log.debug("verified order for quote %d" % (quote_id))
    return verified_order_container


def _get_quote_product_orders(quote_id, mask): # pylint: disable-msg=C0103
    """Generator returning all product order containers for the given quote id"""
    quote_service = get_service('SoftLayer_Billing_Order_Quote', quote_id)
    quote_service.set_object_mask(mask)
    log.debug("fetching order container for quote id %d", quote_id)
    quote_container = quote_service.getRecalculatedOrderContainer()
    for product_order_container in quote_container['orderContainers']:
        yield SoftLayerContainerProductOrder(product_order_container)


def _find_vlan(vlan_type, vlan_spec):
    """Return a single public or private vlan matching spec"""
    log.debug("looking up %s vlan %s" % (vlan_type, vlan_spec))
    vlan_object_mask = build_vlan_object_mask()
    if vlan_type == 'public':
        # Lookup Public VLAN
        vlans = list(get_public_vlans(
            parse_vlan_spec(vlan_spec), vlan_object_mask))
    elif vlan_type == 'private':
        # Lookup Public VLAN
        vlans = list(get_private_vlans(
            parse_vlan_spec(vlan_spec), vlan_object_mask))

    if len(vlans) < 1:
        print error("No vlans found matching spec: %s" % (vlan_spec))
        sys.exit(1)

    if len(vlans) > 1:
        print error("More then one vlan found matching spec: %s. Refusing to continue." % (vlan_spec))
        sys.exit(1)

    return vlans[0]


def quotes(args):
    """Show quotes

    Usage: slapi billing quotes [options] [<quote_spec>]

    Options:
        -F, --format FORMAT
        -h, --help
    """
    # Parse quote_spec
    quote_spec = parse_quote_spec(args['<quote_spec>'])
    # TODO: Build Object Mask
    object_mask = None

    for quote in get_quotes(quote_spec, object_mask):
        print quote.format()


def orderquote(args):
    """Place an order from an existing quote

    Usage: slapi billing orderquote [options] <quote_spec> <hostname> <domain>

    Options:
        --network-public-vlan VLAN_SPEC
        --network-private-vlan VLAN_SPEC
        -h, --help
    """
    # Parse Quote Spec
    quote_spec = parse_quote_spec(args['<quote_spec>'])
    # TODO: Build Object Mask
    object_mask = None

    # Get Quotes
    quotes = list(get_quotes(quote_spec, object_mask))
    if len(quotes) < 1:
        print warning("No quotes found matching spec: %s." % args['<quote_spec>'])
        sys.exit(1)
    if len(quotes) > 1:
        print error("More then one quote matching spec: %s. Refusing to continue." % args['<quote_spec>'])
        sys.exit(1)

    # Get Quote
    quote = quotes[0]
    log.debug("found quote: %d, name: %s, key: %s" % (quote.id, quote.name, quote.key))

    # Get Orders Containers
    order_containers = list(_get_quote_product_orders(quote.id, None))
    if len(order_containers) < 0:
        print error("Quote %d contains no product orders." % (quote.id))
        sys.exit(1)
    if len(order_containers) > 1:
        print error("Quote %d contains more then one product orders. Refusing to continue." % (quote.id))
        sys.exit(1)
    order_container = order_containers[0]

    # Get VLAN information
    if args['--network-public-vlan']:
        public_vlan = _find_vlan('public', args['--network-public-vlan'])
    else:
        public_vlan = None
    if args['--network-private-vlan']:
        private_vlan = _find_vlan('private', args['--network-public-vlan'])
    else:
        private_vlan = None

    # Check public vlan location
    if public_vlan and \
            public_vlan.primary_router.datacenter.id != order_container.location.id:
        print error("Public VLAN %d does not appear to be in %s." % (
            public_vlan.vlan, order_container.location.name))
        sys.exit(1)

    # Check private vlan location
    if private_vlan and \
            private_vlan.primary_router.datacenter.id != order_container.location.id:
        print error("Private VLAN %d does not appear to be in %s." % (
            public_vlan.vlan, order_container.location.name))
        sys.exit(1)

    # Set order type
    order_container._data['complexType'] = 'SoftLayer_Container_Product_Order_Hardware_Server'

    # Get order hardware
    hardware = order_container._data['hardware'][0]

    # Update order information
    hardware['hostname'] = args['<hostname>']
    hardware['domain'] = args['<domain>']

    # Configure VLANs
    if public_vlan:
        hardware['primaryNetworkComponent']['networkVlanId'] = public_vlan.id
    if private_vlan:
        hardware['primaryBackendNetworkComponent']['networkVlanId'] = private_vlan.id

    pp(order_container._data)
    verified_order_container = _verify_order(quote.id, order_container)
    print verified_order_container.format()
    pp(verified_order_container._data)


def orders(args):
    """Show orders

    Usage: slapi billing orders [options] [<order_spec>]

    Options:
        -F, --format FORMAT
        -h, --help

    """
    order_spec = parse_order_spec(args )
    object_mask = None

    for order in get_orders(order_spec, object_mask):
        print order.format()
