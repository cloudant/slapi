from util.softlayer.objects.core import *
from util.softlayer.objects.network import SoftLayerNetworkVLAN
from util.softlayer.objects.network import SoftLayerNetworkSubnet


class SoftLayerHardwareComponentModel(BaseSoftLayerObject):
    """SoftLayer_Hardware_Component_Model"""

    def __init__(self, obj):
        super(SoftLayerHardwareComponentModel, self).__init__(obj)

    @softlayer_property_format(label=False)
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

    @softlayer_property_format(label=False)
    def id(self):  # pylint: disable-msg=C0103
        return self.get_data('id')

    @softlayer_object_property(SoftLayerHardwareComponentModel, label="Model")
    def model(self):
        return self.get_data('hardwareComponentModel')


class SoftLayerNetworkComponent(BaseSoftLayerObject):
    """SoftLayer_Network_Component"""

    def __init__(self, obj):
        super(SoftLayerNetworkComponent, self).__init__(obj)

    @softlayer_property_format(label=False)
    def id(self):  # pylint: disable-msg=C0103
        return self.get_data('id')

    @softlayer_property_format(order=0)
    def name(self):
        return "%s%s" % (self.get_data('name'), str(self.get_data('port')))

    @softlayer_property_format("IP Address", order=1)
    def ip_address(self):
        return self.get_data('primaryIpAddress')

    @softlayer_object_property(SoftLayerNetworkSubnet, order=3)
    def subnet(self):
        return self.get_data('primarySubnet')

    @softlayer_object_property(SoftLayerNetworkVLAN, label="VLAN", order=2)
    def vlan(self):
        if self.subnet:
            return self.subnet.get_data('networkVlan')
        else:
            return None

    @softlayer_property_format(order=4)
    def speed(self):
        return self.get_data('speed')

    @softlayer_property_format(order=4)
    def status(self):
        return self.get_data('status').capitalize()


class SoftLayerHardwareServer(BaseSoftLayerObject):
    """SoftLayer_Hardware_Server"""

    def __init__(self, obj):
        super(SoftLayerHardwareServer, self).__init__(obj)

    @softlayer_property_format(order=0)
    def id(self):  # pylint: disable-msg=C0103
        return self.get_data('id')

    @softlayer_property_format(order=1)
    def hostname(self):
        return self.get_data('hostname')

    @softlayer_property_format(order=2)
    def domain(self):
        return self.get_data('domain')

    @softlayer_property_format(label="FQDN", order=3)
    def fqdn(self):
        return self.get_data('fullyQualifiedDomainName')

    @softlayer_property_format(label="Public IP", order=4)
    def public_ip_address(self):
        return self.get_data('primaryIpAddress')

    @softlayer_property_format(label="Private IP", order=5)
    def private_ip_address(self):
        return self.get_data('primaryBackendIpAddress')

    @softlayer_property_format(label="Management IP", order=6)
    def management_ip_address(self):
        return self.get_data('networkManagementIpAddress')

    @softlayer_object_property(SoftLayerLocation, order=7)
    def datacenter(self):
        return self.get_data('datacenter')

    @softlayer_property_format(order=8)
    def serial_number(self):
        return self.get_data('serialNumber')

    @softlayer_object_property(SoftLayerTransaction,
                               label="Last Transaction", order=10)
    def last_transaction(self):
        return self.get_data('lastTransaction')

    @softlayer_object_property(SoftLayerTransaction,
                               label="Active Transactions", order=11)
    def active_transactions(self):
        return self.get_data('activeTransactions')

    @softlayer_object_property(SoftLayerHardwareComponent,
                               label="Processors", order=12)
    def processors(self):
        return self.get_data('processors')

    @softlayer_object_property(SoftLayerHardwareComponent,
                               label="Disks", order=13)
    def disks(self):
        return self.get_data('hardDrives')

    @softlayer_object_property(SoftLayerHardwareComponent,
                               label="Memory", order=14)
    def memory(self):
        return self.get_data('memory')

    @softlayer_object_property(SoftLayerHardwareComponent,
                               label="Motherboard", order=15)
    def motherboard(self):
        return self.get_data('motherboard')

    @softlayer_object_property(SoftLayerNetworkComponent,
                               label="NICs", order=16)
    def nics(self):
        return self.get_data('networkComponents')
