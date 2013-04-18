from util.softlayer.objects.core import *


class SoftLayerHardwareComponentModel(BaseSoftLayerObject):
    """SoftLayer_Hardware_Component_Model"""

    def __init__(self, obj):
        super(SoftLayerHardwareComponentModel, self).__init__(obj)

    @softlayer_property_format(property_display=False)
    def id(self):  # pylint: disable-msg=C0103
        return self.get_data('id')

    @softlayer_property
    def description(self):
        return self.get_data('description')

    @softlayer_property
    def capacity(self):
        return self.get_data('capacity')

    @softlayer_property
    def manufacturer(self):
        return self.get_data('manufacturer')

    @softlayer_property
    def version(self):
        return self.get_data('version')

    @softlayer_property
    def name(self):
        return self.get_data('name')


class SoftLayerHardwareComponent(BaseSoftLayerObject):
    """SoftLayer_Hardware_Component"""

    def __init__(self, obj):
        super(SoftLayerHardwareComponent, self).__init__(obj)

    @softlayer_property_format(property_display=False)
    def id(self):  # pylint: disable-msg=C0103
        return self.get_data('id')

    @softlayer_object_property(SoftLayerHardwareComponentModel, property_name="Model")
    def model(self):
        return self.get_data('hardwareComponentModel')


class SoftLayerNetworkVLAN(BaseSoftLayerObject):

    def __init__(self, obj):
        super(SoftLayerNetworkVLAN, self).__init__(obj)

    @softlayer_property_format(property_display=False)
    def id(self):  # pylint: disable-msg=C0103
        return self.get_data('id')

    @softlayer_property_format(property_display="VLAN")
    def vlan(self):
        return self.get_data('vlanNumber')


class SoftLayerNetworkSubnet(BaseSoftLayerObject):

    def __init__(self, obj):
        super(SoftLayerNetworkSubnet, self).__init__(obj)

    @softlayer_property_format(property_display=False)
    def id(self):  # pylint: disable-msg=C0103
        return self.get_data('id')

    @softlayer_property
    def netmask(self):
        return self.get_data('netmask')

    @softlayer_property
    def gateway(self):
        return self.get_data('gateway')

    @softlayer_property_format("VLAN")
    def vlan(self):
        return self.get_data('networkVlan')


class SoftLayerNetworkComponent(BaseSoftLayerObject):
    """SoftLayer_Network_Component"""

    def __init__(self, obj):
        super(SoftLayerNetworkComponent, self).__init__(obj)

    @softlayer_property_format(property_display=False)
    def id(self):  # pylint: disable-msg=C0103
        return self.get_data('id')

    @softlayer_property
    def name(self):
        return "%s%s" % (self.get_data('name'), str(self.get_data('port')))

    @softlayer_property_format("IP Address")
    def ip_address(self):
        return self.get_data('primaryIpAddress')

    @softlayer_object_property(SoftLayerNetworkSubnet)
    def subnet(self):
        return self.get_data('primarySubnet')

    @softlayer_property
    def speed(self):
        return self.get_data('speed')

    @softlayer_property
    def status(self):
        return self.get_data('status').capitalize()


class SoftLayerHardwareServer(BaseSoftLayerObject):
    """SoftLayer_Hardware_Server"""

    def __init__(self, obj):
        super(SoftLayerHardwareServer, self).__init__(obj)

    @softlayer_property_format("Id")
    def id(self):  # pylint: disable-msg=C0103
        return self.get_data('id')

    @softlayer_property_format("AccountId")
    def account_id(self):
        return self.get_data('accountId')

    @softlayer_property
    def domain(self):
        return self.get_data('domain')

    @softlayer_property
    def hostname(self):
        return self.get_data('hostname')

    @softlayer_property_format("FQDN")
    def fqdn(self):
        return self.get_data('fullyQualifiedDomainName')

    @softlayer_property_format("Public IP")
    def public_ip_address(self):
        return self.get_data('primaryIpAddress')

    @softlayer_property_format("Private IP")
    def private_ip_address(self):
        return self.get_data('primaryBackendIpAddress')

    @softlayer_property_format("Management IP")
    def management_ip_address(self):
        return self.get_data('networkManagementIpAddress')

    @softlayer_property
    def serial_number(self):
        return self.get_data('serialNumber')

    @softlayer_object_property(SoftLayerLocation)
    def datacenter(self):
        return self.get_data('datacenter')

    @softlayer_object_property(SoftLayerTransaction, property_name="Last Transaction")
    def last_transaction(self):
        return self.get_data('lastTransaction')

    @softlayer_object_property(SoftLayerTransaction, property_name="Active Transactions")
    def active_transactions(self):
        return self.get_data('activeTransactions')

    @softlayer_object_property(SoftLayerHardwareComponent, property_name="Processors")
    def processors(self):
        return self.get_data('processors')

    @softlayer_object_property(SoftLayerHardwareComponent, property_name="Disks")
    def disks(self):
        return self.get_data('hardDrives')

    @softlayer_object_property(SoftLayerHardwareComponent, property_name="Memory")
    def memory(self):
        return self.get_data('memory')

    @softlayer_object_property(SoftLayerHardwareComponent, property_name="Motherboard")
    def motherboard(self):
        return self.get_data('motherboard')

    @softlayer_object_property(SoftLayerNetworkComponent, property_name="NICs")
    def nics(self):
        return self.get_data('networkComponents')
