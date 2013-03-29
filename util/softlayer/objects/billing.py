from util.softlayer.objects.core import *

class SoftLayerBillingOrder(BaseSoftLayerObject):
    """SoftLayer_Billing_Order"""

    def __init__(self, obj):
        super(SoftLayerBillingOrder, self).__init__(obj)

    @softlayer_property_format(property_display=False)
    def id(self):
        return self.data['id']

    @softlayer_property
    def status(self):
        return self.data['status']

    @softlayer_property
    def create_date(self):
        return self.data['createDate']

class SoftLayerBillingOrderQuote(BaseSoftLayerObject):
    """SoftLayer_Billing_Order_Quote"""

    def __init__(self, obj):
        super(SoftLayerBillingOrderQuote, self).__init__(obj)

    @softlayer_property_format(property_display=False)
    def id(self):
        return self.data['id']

    @softlayer_property
    def name(self):
        return self.data['name']

    @softlayer_property
    def status(self):
        return self.data['status']

    @softlayer_property
    def key(self):
        return self.data['quoteKey']

    @softlayer_property
    def create_date(self):
        return self.data['createDate']
