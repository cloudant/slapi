import re

PATTERN_OBJECT_ID = re.compile(r'^(\d+)$')
PATTERN_IP_ADDRESS = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
PATTERN_VLAN_NUMBER = re.compile(r'^(\d+)$')

def _identity_spec(obj):
    return True


def parse_order_spec(args):
    return _identity_spec


def parse_subnet_spec(args):
    return _identity_spec


def parse_vlan_spec(spec):
    if spec is None:
        return _identity_spec

    # match vlan number 
    match = PATTERN_VLAN_NUMBER.match(spec)
    if match:
        object_id = int(match.group(1))
        # return function matching object id
        return lambda obj: int(obj['vlanNumber']) == object_id

    raise TypeError("Unknown VLAN spec: %s" % (spec))


def parse_location_spec(spec):
    if spec is None:
        return _identity_spec

    # match object id
    match = PATTERN_OBJECT_ID.match(spec)
    if match:
        object_id = int(match.group(1))
        # return function matching object id
        return lambda o: int(o['id']) == object_id 

    # match quote name
    datacenter_name = spec
    return lambda d: re.search(datacenter_name, d['name']) != None


def parse_quote_spec(spec):
    """
    quote_spec := object_id | name
    """
    if spec is None:
        return _identity_spec

    # match quote object id
    match = PATTERN_OBJECT_ID.match(spec)
    if match:
        quote_id = int(match.group(1))
        # return function matching quote object id
        return lambda q: int(q['id']) == quote_id

    # match quote name
    quote_name = spec
    return lambda q: re.search(quote_name, q['name']) != None

def parse_hardware_spec(args):
    """
    hardware_spec := object_id | ip_address | fqdn
    """
    # Check for hardware spec argument
    if '<hardware_spec>' in args:
        spec = args['<hardware_spec>']
        if spec is None:
            return _identity_spec

        # match hardware object id 
        match = PATTERN_OBJECT_ID.match(spec)
        if match:
            hardware_id = int(match.group(1))
            # return function matching hardware object id
            return lambda h: int(h['id']) == hardware_id

        # Match hardware ip
        match = PATTERN_IP_ADDRESS.match(spec)
        if match:
            hardware_address = spec
            # return functing matching ip address
            return lambda h: (h['primaryIpAddress'] == hardware_address or
                h['primaryBackendIpAddress'] == hardware_address)

        # Match hardware fqdn
        hardware_name = spec
        return lambda h: re.search(hardware_name, h['fullyQualifiedDomainName']) != None
    else:
        # return identity spec (matches all objects)
        return _identity_spec
