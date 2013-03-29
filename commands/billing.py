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
from util.softlayer.service import *
from util.softlayer.objects.billing import *

def _get_quotes(quote_spec, mask):
    """Generator returning all quotes matching quote_spec"""
    for obj in get_objects('SoftLayer_Billing_Order_Quote', 'getQuotes', quote_spec, mask):
        yield SoftLayerBillingOrderQuote(obj)

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
