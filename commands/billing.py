"""usage: slapi [options] billing <command> [<args>...]

options:
    -v, --verbose
    -h, --help

commands:
    billing quotes          Show quotes
    billing orders          Show orders
    billing placeorder      Place an order
"""
from util.helpers import *
from util.spec import *
from util.config import config
from util.log import log
from util.softlayer.service import get_objects, get_service
from util.softlayer.objects.billing import *

def _get_quotes(quote_spec, mask):
    """Generator returning all quotes matching quote_spec"""
    for obj in get_objects('SoftLayer_Billing_Order_Quote', 'getQuotes', quote_spec, mask):
        yield SoftLayerBillingOrderQuote(obj)

def _get_quote_product_order_container(quote_id, mask):
    quote_service = get_service('SoftLayer_Billing_Order_Quote', quote_id)
    quote_service.set_object_mask(mask)
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
    # TODO: Parse quote_spec
    quote_spec = identity_spec
    object_mask = None

    for quote in _get_quotes(quote_spec, object_mask):
        print quote.format()
        for order in _get_quote_product_order_container(quote.id, None):
            print order.format()

def orders(args):
    """usage: slapi billing orders [options] [<order_spec>]

    options:

    """
    # TODO: Parse order_spec
    order_spec = identity_spec
    object_mask = None

    for order in _get_orders(order_spec, object_mask):
        print order.format()

def placeorder(args):
    """usage: slapi billing placeorder [options]

    options:

    """
    pass
