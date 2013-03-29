import SoftLayer.API

from util.helpers import *
from util.log import log
from util.config import config

def get_objects(service_name, service_method_name, spec, mask):
    account_service = get_service('SoftLayer_Account')
    account_service.set_object_mask(None)
    log.debug("fetching all %s objects with %s" % (service_name, spec))
    for obj in filter(spec, account_service.__getattr__(service_method_name)()):
        log.debug("fetching object id %d" % (obj['id']))
        service = get_service(service_name, obj['id'])
        service.set_object_mask(mask)
        yield service.getObject()

def get_service(name, object_id=None):
    api_user = config['softlayer']['api_user']
    api_key = config['softlayer']['api_key']
    return SoftLayer.API.Client(name, object_id, api_user, api_key)

