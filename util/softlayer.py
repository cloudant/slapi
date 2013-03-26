import os
import sys
import SoftLayer.API

from util.config import config

def get_account_service(object_id=None):
    return _get_service('SoftLayer_Account', object_id)

def get_hardware_server_service(object_id=None):
    return _get_service('SoftLayer_Hardware_Server', object_id)

def _get_service(name, object_id=None):
    api_user = config['softlayer']['api_user']
    api_key = config['softlayer']['api_key']
    return SoftLayer.API.Client(name, object_id, api_user, api_key)
