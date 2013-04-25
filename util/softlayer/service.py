import SoftLayer.API

from util.log import log
from util.config import config
from util.softlayer.objects.network import SoftLayerNetworkVLAN
from util.softlayer.objects.network import SoftLayerNetworkSubnet
from util.softlayer.objects.billing import SoftLayerBillingOrderQuote
from util.softlayer.objects.billing import SoftLayerBillingOrder

def get_objects(service_name, service_method_name, spec, mask):
    """Generator returning all objects for from a SoftLayer service"""
    account_service = get_service('SoftLayer_Account')
    account_service.set_object_mask(None)
    log.debug("fetching all %s objects with %s", service_name, spec)
    for obj in filter(spec, account_service.__getattr__(service_method_name)()):
        log.debug("fetching object id %d", obj['id'])
        service = get_service(service_name, obj['id'])
        service.set_object_mask(mask)
        yield service.getObject()


def get_service(name, object_id=None):
    """Return a SoftLayer service with the given name"""
    api_user = config['softlayer']['api_user']
    api_key = config['softlayer']['api_key']
    return SoftLayer.API.Client(name, object_id, api_user, api_key)


#==============================================================================
# Object Mask
#==============================================================================


def build_subnet_object_mask(**kwargs):
    object_mask = dict()
    object_mask['networkVlan'] = {}
    return object_mask


def build_vlan_object_mask(include_routers=True, include_subnets=False):
    object_mask = dict()
    if include_routers:
        object_mask['primaryRouter'] = dict()
        object_mask['primaryRouter']['datacenter'] = dict()
        object_mask['secondaryRouter'] = dict()
        object_mask['secondaryRouter']['datacenter'] = dict()
    if include_subnets:
        object_mask['primarySubnet'] = dict()
        object_mask['additionalPrimarySubnets'] = dict()
        object_mask['secondarySubnets'] = dict()
    return object_mask


#==============================================================================
# Billing
#==============================================================================


def get_quotes(quote_spec, mask):
    """Generator returning all quotes matching quote_spec"""
    for obj in get_objects('SoftLayer_Billing_Order_Quote', 'getQuotes', quote_spec, mask):
        yield SoftLayerBillingOrderQuote(obj)


def get_orders(order_spec, mask):
    """Generator returning all orders matching quote_spec"""
    for obj in get_objects('SoftLayer_Billing_Order', 'getOrders', order_spec, mask):
        yield SoftLayerBillingOrder(obj)


#==============================================================================
# Network
#==============================================================================


def get_subnets(subnet_spec, mask):
    """Generator returning network subnets matching subnet_spec"""
    for obj in get_objects('SoftLayer_Network_Subnet', 'getSubnets', subnet_spec, mask):
        yield SoftLayerNetworkSubnet(obj)


def get_vlans(vlan_spec, mask):
    """Generator returning primary network vlans matching subnet_spec"""
    for obj in get_objects('SoftLayer_Network_Vlan', 'getNetworkVlans', vlan_spec, mask):
        yield SoftLayerNetworkVLAN(obj)


def get_public_vlans(vlan_spec, mask):
    """Generator returning public network vlans matching vlan_spec"""
    for obj in get_objects('SoftLayer_Network_Vlan', 'getPublicNetworkVlans', vlan_spec, mask):
        yield SoftLayerNetworkVLAN(obj)


def get_private_vlans(vlan_spec, mask):
    """Generator returning private network vlans matching vlan_spec"""
    for obj in get_objects('SoftLayer_Network_Vlan', 'getPrivateNetworkVlans', vlan_spec, mask):
        yield SoftLayerNetworkVLAN(obj)
