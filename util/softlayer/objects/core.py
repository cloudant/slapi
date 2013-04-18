import string # pylint: disable-msg=W0402

from util.helpers import format_object

class softlayer_property(object): # pylint: disable-msg=C0103
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

def softlayer_property_format(property_name=None, property_display=True): 
    """factory function for softlayer_property__format_decorator"""
    def softlayer_property_format_decorator(func): # pylint: disable-msg=C0103
        @softlayer_property
        def wrapped_f(*args):
            return func(*args)
        # set property_format
        wrapped_f.property_name = property_name
        wrapped_f.property_display = property_display
        return wrapped_f
    return softlayer_property_format_decorator

def softlayer_object_property(object_type, property_name=None, property_display=True):
    """factory function for softlayer_object_property_decorator"""
    def softlayer_object_property_decorator(func): # pylint: disable-msg=C0103
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
        wrapped_f.property_name = property_name
        wrapped_f.property_display = property_display
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

    def format(self, mask=None, only_locals=False, color=True):
        obj = self._format(mask, only_locals)
        return format_object(obj, color=color)

    def _format(self, mask, only_locals):
        obj = {}
        #TODO: sort local first?
        for key, method in self.__class__.__dict__.iteritems():
            if isinstance(method, softlayer_property):
                property_display = getattr(method, 'property_display', True)
                if not property_display:
                    continue

                property_name = getattr(method, 'property_name', key)
                if property_name is None or property_name == key:
                    property_name = string.capwords(' '.join(key.split('_')))

                property_value = method.__get__(self, key)
                if isinstance(property_value, list):
                    # format each item in the list
                    obj[property_name] = list()
                    for property_value_item in property_value:
                        obj[property_name].append(property_value_item._format(mask, only_locals))

                elif isinstance(property_value, BaseSoftLayerObject):
                    if property_value is not None:
                        obj[property_name] = property_value._format(mask, only_locals)
                else:
                    if property_value is not None:
                        obj[property_name] = property_value
        return obj

class SoftLayerLocation(BaseSoftLayerObject):
    """SoftLayer_Location"""

    def __init__(self, obj):
        super(SoftLayerLocation, self).__init__(obj)

    @softlayer_property_format(property_display=False)
    def id(self):
        return self.get_data('id')

    @softlayer_property_format("Short Name")
    def name(self):
        return self.get_data('name')

    @softlayer_property_format("Name")
    def pretty_name(self):
        return self.get_data('longName')

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
