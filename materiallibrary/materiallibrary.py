""" Mimic the 'Airtable' database
"""

from . import pythontools as pytool

import numpy as np

class Property(object):
    """Physical property Class

    Contains the name, the symbol, the unit, and additional tags
    """

    def __init__(self, Symbol, Name, unit, tags=[], **kwargs):
        self.symbol = Symbol
        self.name = Name
        self.unit = unit
        self.tags = tags

    def __repr__(self):
        return "<Prop. {}, {} ({})>".format(self.symbol,
                                            self.name, self.unit)
    # TODO unit convert method


class Value(object):
    """Store the float value of a physical property."""

    def __init__(self, phiproperty, value, material=None,
                 minmax=None, temp=None, source=None, **kwargs):
        """
        value: float, physical value
        source: string, url or reference about the source
                of the information
        """
        self.material = material
        self.property = phiproperty
        self.value = value
        self.source = source
        self.minmax = minmax    # range
        self.temp = temp

    def __repr__(self):
        return '<Val. {}={} {}>'.format(self.property.symbol,
                                        self.value, self.property.unit)


class CollectionOfValues(object):
    """Groups of many values of the same property and material.
    """

    def __init__(self, values):
        """  values: list of Value Object
        """
        self.valuelist = [v.value for v in values]

        properties = {v.property for v in values}
        if len(properties) > 1:
            print('attention : more than one property')
        else:
            self.property = list(properties)[0]

        self.min = min(self.valuelist)
        self.max = max(self.valuelist)
        self.mean = sum(self.valuelist) / len(self.valuelist)

        self.attributes = {
            'min': lambda x: min(x.valuelist),
            'max': lambda x: max(x.valuelist),
            'mean': lambda x: sum(x.valuelist) / len(x.valuelist),
            'unit': lambda x: x.property.unit,
            'array': lambda x: np.array(x.valuelist)
            }
        self.default = self.attributes['mean']

    def addallattributes(self, parentself):
        for suffix, fun in self.attributes.items():
            name = '_'.join( ( self.property.symbol, suffix ) )
            setattr( parentself, name, fun(self) )

        # default:
        setattr( parentself, self.property.symbol, self.default(self) )


class Material(object):
    """Material object. Groups the values.

        for the property P
        self.P >> defaut value
        self.P_min
        self.P_max
        self.P_values

        self.values
    """

    def __init__(self, name, values=[], tags=[], chemicalcomp='', **kwargs):
        """ values : list of object Value
        """
        self.name = name
        self.tags = tags
        self.chemicalcomp = chemicalcomp

        self.properties = set()  # set of used property
        self.values = values

        # Create dynamically the attributes:
        if self.values:
            self.update()


    def __repr__(self):
        return "<Mat. {}>".format(self.name)

    def addvalue(self, value, update=True):
        self.values.append(value)
        if update:
            self.update

    def update(self):
        """ Create dynamically the properties attributes for the material
        """

        # tidy the values by property
        sorted_values = {}
        for value in self.values:
            pytool.dictappend(sorted_values, value.property, value)

        for prop, values in sorted_values.items():
            # populate the self.properties dict
            self.properties.add(prop)

            # -- object Collection of Values
            collect = CollectionOfValues(values)
            collect.addallattributes(self) # appends _min, _max...etc attributes


    def addvalue_old(self, value):
        """ add a value to the material (i.e. to the .P_values list)
            value is a Value Object
        """
        symbol = value.property.symbol
        attrname = symbol + '_values'
        if hasattr(self, attrname):
            valuelist = getattr(self, attrname)
            valuelist.append(value)
        else:
            setattr(self, attrname, [value, ])


class Library(object):
    """ The place to store the materials

        Attributes
            properties : dict of the physical properties used by the materials
                key are the symbol
            materials : dict of the material object
    """
    # todo: search & filter

    def __init__(self):

        self.properties = {}
        self.materials = {}
        pass

    def addmaterial(self, material):
        """ add a material

        Argument:
            material: a material object
        """
        key = material.name
        if key in self.materials:
            print(' %s already exist ' % key)
        else:
            self.materials[key] = material

    def addproperty(self, newproperty):
        """Add a property to the properties dict.

        The property symbol is used as key

        Argument:
            property: a Property Object
        """
        key = newproperty.symbol
        if key in self.properties:
            print(' %s already exist ' % key)
            # Todo : replace ?
        else:
            self.properties[key] = newproperty

    def filter(self, properties=None, tags=None):
        """Return the list of materials corresponding to the filter.

        - where all the properties are defined
        - where all the tags are present

        """
        def matfilter(mat):
            pass

        filtered = [m for m in self.materials if matfilter(m)]

        return filtered
