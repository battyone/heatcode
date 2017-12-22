""" Mimic the 'Airtable' database
"""

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
        self.values = Values # ... to process

    def __repr__(self):
        return "{} - {} ({})".format( self.symbol,
        self.name, self.unit )
    # Todo: unit convert method

class Value(object):
    """
    """

    def __init__(self, material, phiproperty, value, minmax=None, temp=None):
        self.material = material
        self.property = phiproperty
        self.value = value
        self.minmax = minmax # range
        self.temp = temp


class Material(object):
    """
    """

    def __init__(self, Name, defined_properties=[], Values=[], tags=[]):
        self.name = Name
        self.defined_properties = defined_properties
        self.values = Values
        self.tags = tags

        # setattr(self, name, value)

    # Todo: print

class Library(object):
    """ The place to store the materials
    """
    def __init__(self):
        pass

    def add(self, material):
        pass

    @property
    def properties(self):
        """ dict of the physical properties used by the materials
        """
        pass
