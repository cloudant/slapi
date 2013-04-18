import re

PATTERN_OBJECTID = re.compile(r'^(\d+)$')
PATTERN_IPADDR = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')

def identity_spec(o):
    return True

def parse_quote_spec(args):
    pass

def parse_hardware_spec(args):
    """
    hardware_spec := object_id | ip_address | fqdn
    """
    # Check for hardware spec argument
    if '<hardware_spec>' in args:
        spec = args['<hardware_spec>']

        # Match hardware id
        match = PATTERN_OBJECTID.match(spec)
        if match:
            hardware_id = int(match.group(1))
            return lambda h: int(h['id']) == hardware_id

        # Match hardware ip
        match = PATTERN_IPADDR.match(spec)
        if match:
            hardware_address = spec 
            return lambda h: (h['primaryIpAddress'] == hardware_address or
                h['primaryBackendIpAddress'] == hardware_address)

        # Match hardware fqdn
        hardware_name = spec
        return lambda h: re.search(hardware_name, h['fullyQualifiedDomainName']) != None
    else:
        return identity_spec
