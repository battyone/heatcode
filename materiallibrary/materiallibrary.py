""" Mimic the 'Airtable' database
"""

from . import pythontools as pytool


class Property(object):
    """ Physical property Class
        contains the unit, name, abbreviation,
        the field tags
    """
    def __init__(self, Symbol, Name, unit, tags=[], Values=[]):
        self.symbol = Symbol
        self.name = Name
        self.unit = unit
        self.tags = tags
        self.values = Values

    def __repr__(self):
        return "<Prop. {}, {} ({})>".format(self.symbol,
                                            self.name, self.unit)
    # Todo: unit convert method


class Value(object):
    """ Store the float value of a physical property
    """

    def __init__(self, phiproperty, value, material=None,
                 minmax=None, temp=None, source=None):
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
    """ groups of many values of the same property and material
    """

    def __init__(self, values):
        """  values: list of Value Object
        """
        self.valuelist = [v.value for v in values]
        self.property = {v.property for v in values}
        if len(self.property) > 1:
            print('attention : more than one property')

        self.min = min(self.valuelist)
        self.max = max(self.valuelist)
        self.mean = sum(self.valuelist) / len(self.valuelist)


class Material(object):
    """

        for the property P
        self.P >> defaut value
        self.P_min
        self.P_max
        self.P_values

        self.values
    """

    def __init__(self, name, values=[], tags=[], chemicalcomp=''):
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

        # setattr(self, name, value)
        # self.pp = property(fget=, fset=)

    def __repr__(self):
        return "<Mat. {}>".format(self.name)

    def addvalue(self, value, update=True):
        self.values.append(value)
        if update:
            self.update

    def update(self):
        """ Create dynamically the properties attr for the material
        """

        # tidy the values by property
        sorted_values = {}
        for value in self.values:
            pytool.dictappend(sorted_values, value.property, value)

        for prop, values in sorted_values.items():
            # populate the self.properties dict
            self.properties.add(prop)

            # ... need object Collection of Values
            collect = CollectionOfValues(values)

            propname_default = prop.symbol
            setattr(self, propname_default, collect.mean)
            propname_min = prop.symbol + '_min'
            setattr(self, propname_min, collect.min)
            propname_max = prop.symbol + '_max'
            setattr(self, propname_max, collect.max)
            # todo : automatiser ?

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
        """ add a property to the properties dict
            use the symbol as key
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
        """ return the list of materials corresponding to the filter

            - where all the properties are defined
            - where all the tags are present

        """
        pass
