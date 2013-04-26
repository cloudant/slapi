import string  # pylint: disable-msg=W0402

from collections import OrderedDict
from util.formatting import format_object


class softlayer_property(object):  # pylint: disable-msg=C0103
    def __init__(self, method):
        self.method = method
        self.__name__ = method.__name__
        self.__doc__ = method.__doc__

    def __get__(self, obj, cls=None):
        result = self.method(obj)
        return result

    def __set__(self, obj, value):
        raise AttributeError("This property is read-only")

    def __delete__(self, inst):
        raise AttributeError("This property is read-only")


def softlayer_property_format(label=None, order=1000):
    """factory function for softlayer_property__format_decorator"""
    def softlayer_property_format_decorator(func):  # pylint: disable-msg=C0103
        @softlayer_property
        def wrapped_f(*args):
            return func(*args)
        # set property formatting attributes
        wrapped_f.property_label = label
        wrapped_f.property_order = order
        return wrapped_f
    return softlayer_property_format_decorator


def softlayer_object_property(object_type, label=None, order=1000):
    """factory function for softlayer_object_property_decorator"""
    def softlayer_object_property_decorator(func):  # pylint: disable-msg=C0103
        @softlayer_property
        def wrapped_f(*args):
            data = func(*args)
            if isinstance(data, list):
                objects = []
                for obj in data:
                    objects.append(object_type(obj))
                return objects
            else:
                if data is None:
                    return None
                else:
                    obj = data
                    return object_type(obj)
        wrapped_f.property_label = label
        wrapped_f.property_order = order
        return wrapped_f
    return softlayer_object_property_decorator


class BaseSoftLayerObject(object):
    """Base SoftLayer Object"""

    def __init__(self, obj):
        self._data = obj

    def get_data(self, key, default=None, raise_error=False):
        if key in self._data:
            return self._data[key]
        else:
            if raise_error:
                raise KeyError("No such key: %s" % (key))
            else:
                return default

    def format(self, format='text', color=True):
        obj = self._format()
        return format_object(obj, color=color)

    def _gather_properties_to_format(self):
        """Generator returning tuples of (key, attr) of properties to format"""
        # built a list of tuples of (key, property_order)
        keys = list()
        for key, method in self.__class__.__dict__.iteritems():
            # Get property ordering info, default=1000
            property_order = getattr(method, 'property_order', 1000)
            keys.append((key, property_order))

        # build ordered dict from keys sorted by property_order
        for key, _order in sorted(keys, key=lambda i: i[1]):
            yield (key, self.__class__.__dict__[key])

    def _format(self):
        obj = OrderedDict()
        #TODO: sort local first?
        for key, method in self._gather_properties_to_format():
            if isinstance(method, softlayer_property):

                # Get property label
                property_label = getattr(method, 'property_label', key)

                if property_label is False:
                    # If label is false, dont format
                    continue
                elif property_label is None or property_label == key:
                    # If label is None, assume format is just the keyname
                    property_label = string.capwords(' '.join(key.split('_')))

                # Get property value
                property_value = method.__get__(self, key)
                if isinstance(property_value, list):
                    # format each item in the list
                    obj[property_label] = list()
                    for property_value_item in property_value:
                        obj[property_label].append(property_value_item._format())

                elif isinstance(property_value, BaseSoftLayerObject):
                    if property_value is not None:
                        obj[property_label] = property_value._format()
                else:
                    if property_value is not None:
                        obj[property_label] = property_value
        return obj


class SoftLayerAccountAddress(BaseSoftLayerObject):
    """SoftLayer_Account_Address"""

    def __init__(self, obj):
        super(SoftLayerAccountAddress, self).__init__(obj)

    @softlayer_property_format(label=False)
    def id(self):
        return self.get_data('id')

    @softlayer_property_format(label="Address Line 1", order=0)
    def address1(self):
        return self.get_data('address1')

    @softlayer_property_format(label="Address Line 2", order=1)
    def address2(self):
        return self.get_data('address2')

    @softlayer_property_format(order=2)
    def city(self):
        return self.get_data('city')

    @softlayer_property_format(order=4)
    def state(self):
        return self.get_data('state')

    @softlayer_property_format(order=5)
    def zip(self):
        return self.get_data('postalCode')

    @softlayer_property_format(order=6)
    def country(self):
        return self.get_data('country')


class SoftLayerLocation(BaseSoftLayerObject):
    """SoftLayer_Location"""

    def __init__(self, obj):
        super(SoftLayerLocation, self).__init__(obj)

    @softlayer_property_format(label=False)
    def id(self):
        return self.get_data('id')

    @softlayer_property_format(label="Short Name", order=1)
    def name(self):
        return self.get_data('name')

    @softlayer_property_format(label="Name", order=0)
    def pretty_name(self):
        return self.get_data('longName')

    @softlayer_object_property(SoftLayerAccountAddress, order=3)
    def address(self):
        return self.get_data('locationAddress')


class SoftLayerTransactionGroup(BaseSoftLayerObject):
    """SoftLayer_Provisioning_Version1_Transaction_Group"""

    def __init__(self, obj):
        super(SoftLayerTransactionGroup, self).__init__(obj)

    @softlayer_property
    def name(self):
        return self.get_data('name')

    @softlayer_property
    def average_time(self):
        return self.get_data('averageTimeToComplete')


class SoftLayerTransactionStatus(BaseSoftLayerObject):
    """SoftLayer_Provisioning_Version1_Transaction_Status"""

    def __init__(self, obj):
        super(SoftLayerTransactionStatus, self).__init__(obj)

    @softlayer_property
    def name(self):
        if 'friendlyName' in self._data:
            return self.get_data('friendlyName')
        else:
            return self.get_data('name')


class SoftLayerTransaction(BaseSoftLayerObject):
    """SoftLayer_Provisioning_Version1_Transaction"""

    def __init__(self, obj):
        super(SoftLayerTransaction, self).__init__(obj)

    @softlayer_property
    def create_date(self):
        return self.get_data('createDate')

    @softlayer_property
    def modify_date(self):
        return self.get_data('modifyDate')

    @softlayer_object_property(SoftLayerTransactionStatus)
    def status(self):
        return self.get_data('transactionStatus')

    @softlayer_object_property(SoftLayerTransactionGroup)
    def group(self):
        return self.get_data('transactionGroup')
