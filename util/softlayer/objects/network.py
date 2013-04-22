from util.softlayer.objects.core import *

class SoftLayerHardwareRouter(BaseSoftLayerObject):
    """SoftLayer_Hardware_Router"""

    def __init__(self, obj):
        super(SoftLayerHardwareRouter, self).__init__(obj)

    @softlayer_property_format(order=0)
    def id(self):  # pylint: disable-msg=C0103
        return self.get_data('id')

    @softlayer_property_format(label=False)
    def domain(self):
        return self.get_data('domain')

    @softlayer_property_format(order=1)
    def hostname(self):
        return self.get_data('hostname')

class SoftLayerNetworkSubnet(BaseSoftLayerObject):

    def __init__(self, obj):
        super(SoftLayerNetworkSubnet, self).__init__(obj)

    @softlayer_property_format(label=False)
    def id(self):  # pylint: disable-msg=C0103
        return self.get_data('id')

    @softlayer_property_format(order=2)
    def netmask(self):
        return self.get_data('netmask')

    @softlayer_property_format(order=1)
    def gateway(self):
        return self.get_data('gateway')

    @softlayer_property_format(order=0)
    def subnet_type(self):
        return self.get_data('subnetType')


class SoftLayerNetworkVLAN(BaseSoftLayerObject):

    def __init__(self, obj):
        super(SoftLayerNetworkVLAN, self).__init__(obj)

    @softlayer_property_format(label=False)
    def id(self):  # pylint: disable-msg=C0103
        return self.get_data('id')

    @softlayer_property_format("VLAN Number", order=0)
    def vlan(self):
        return self.get_data('vlanNumber')

    @softlayer_object_property(SoftLayerNetworkSubnet, order=1)
    def primary_subnet(self):
        return self.get_data('primarySubnet')

    @softlayer_object_property(SoftLayerNetworkSubnet, order=2)
    def additional_primary_subnets(self):
        return self.get_data('additionalPrimarySubnets')

    @softlayer_object_property(SoftLayerNetworkSubnet, order=3)
    def secondary_subnets(self):
        return self.get_data('secondarySubnets')

    @softlayer_object_property(SoftLayerHardwareRouter, order=4)
    def primary_router(self):
        return self.get_data('primaryRouter')

    @softlayer_object_property(SoftLayerHardwareRouter, order=5)
    def secondary_router(self):
        return self.get_data('secondaryRouter')
