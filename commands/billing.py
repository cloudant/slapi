"""usage: slapi [options] billing <command> [<args>...]

options:
    -v, --verbose
    -h, --help

commands:
    billing quotes          Show quotes
    billing orders          Show orders
    billing placeorder      Place an order
"""
from util.spec import parse_quote_spec, parse_order_spec
from util.config import config
from util.log import log
from util.softlayer.service import get_objects, get_service
from util.softlayer.objects.billing import SoftLayerBillingOrderQuote
from util.softlayer.objects.billing import SoftLayerBillingOrder
from util.softlayer.objects.billing import SoftLayerContainerProductOrder

def _get_quotes(quote_spec, mask):
    """Generator returning all quotes matching quote_spec"""
    for obj in get_objects('SoftLayer_Billing_Order_Quote', 'getQuotes', quote_spec, mask):
        yield SoftLayerBillingOrderQuote(obj)


def _get_quote_product_order_container(quote_id, mask): # pylint: disable-msg=C0103
    """Generator returning all product order containers for the given quote id"""
    quote_service = get_service('SoftLayer_Billing_Order_Quote', quote_id)
    quote_service.set_object_mask(mask)
    log.debug("fetching order container for quote id %d", quote_id)
    quote_container = quote_service.getRecalculatedOrderContainer()
    for product_order_container in quote_container['orderContainers']:
        yield SoftLayerContainerProductOrder(product_order_container)


def _get_orders(order_spec, mask):
    """Generator returning all orders matching quote_spec"""
    for obj in get_objects('SoftLayer_Billing_Order', 'getOrders', order_spec, mask):
        yield SoftLayerBillingOrder(obj)


def quotes(args):
    """usage: slapi billing quotes [options] [<quote_spec>]

    options:

    """
    # Parse quote_spec
    quote_spec = parse_quote_spec(args)
    object_mask = None

    for quote in _get_quotes(quote_spec, object_mask):
        print quote.format()
        for order in _get_quote_product_order_container(quote.id, None):
            print order.format()
            from pprint import pprint as pp
            pp(order._data)


def orders(args):
    """usage: slapi billing orders [options] [<order_spec>]

    options:

    """
    # TODO: Parse order_spec
    order_spec = parse_order_spec(args )
    object_mask = None

    for order in _get_orders(order_spec, object_mask):
        print order.format()


def placeorder(args):
    """usage: slapi billing placeorder [options]

    options:

    """
    pass
