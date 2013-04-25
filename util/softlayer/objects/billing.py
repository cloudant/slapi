from util.softlayer.objects.core import *

class SoftLayerBillingOrder(BaseSoftLayerObject):
    """SoftLayer_Billing_Order"""

    def __init__(self, obj):
        super(SoftLayerBillingOrder, self).__init__(obj)

    @softlayer_property_format(label=False)
    def id(self):
        return self.get_data('id')

    @softlayer_property
    def status(self):
        return self.get_data('status')

    @softlayer_property
    def create_date(self):
        return self.get_data('createDate')

class SoftLayerBillingOrderQuote(BaseSoftLayerObject):
    """SoftLayer_Billing_Order_Quote"""

    def __init__(self, obj):
        super(SoftLayerBillingOrderQuote, self).__init__(obj)

    @softlayer_property_format(label=False)
    def id(self):
        return self.get_data('id')

    @softlayer_property
    def name(self):
        return self.get_data('name')

    @softlayer_property
    def status(self):
        return self.get_data('status')

    @softlayer_property
    def key(self):
        return self.get_data('quoteKey')

    @softlayer_property
    def create_date(self):
        return self.get_data('createDate')

class SoftLayerContainerProductOrder(BaseSoftLayerObject):
    """SoftLayer_Container_Product_Order"""

    def __init__(self, obj):
        super(SoftLayerContainerProductOrder, self).__init__(obj)

    @softlayer_property_format(label="Recurring Cost", order=0)
    def post_tax_recurring_charge(self):
        return self.get_data('postTaxRecurring')

    @softlayer_property_format(label=False)
    def pre_tax_recurring_charge(self):
        return self.get_data('preTaxRecurring')

    @softlayer_property_format(label="Setup Cost", order=1)
    def post_tax_setup_charge(self):
        return self.get_data('postTaxSetup')

    @softlayer_property_format(label=False)
    def pre_tax_setup_charge(self):
        return self.get_data('preTaxSetup')

    @softlayer_property_format(label="Prorated Order Charge", order=2)
    def prorated_order_charge(self):
        return self.get_data('proratedOrderTotal')

    @softlayer_property_format(label=False)
    def currency_type(self):
        return self.get_data('currencyShortName')

    @softlayer_object_property(SoftLayerLocation, order=-1)
    def location(self):
        return self.get_data('locationObject')
