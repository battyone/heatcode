"""Import from the airtable database.

airtable.com provides online relational like database easily editable.

The datebase should be structured using 3 tables as follow :

        Table Materials
            Name (string), unique
            [tags] (list of string)
            [ChemicalFormula] (string)

        Table Values
            id
            material_id
            property_id
            value (float)
            [source] (string)

        Table Properties
            symbol (string), unique
            unit (string)

"""

from . import materiallibrary as ml
from . import pythontools as pytool

import json
from airtable import airtable
# https://github.com/nicocanali/airtable-python
# https://github.com/nicocanali/airtable-python/issues/10


def connection(filename):
    """Get the api-key and database id from the configuration file.

    filename : path to the json config file.
    Return an AirTable connection object.

    The configuration file is as follow (json):
            {
            "apikey":"MY--KEY",
            "baseid":"MY--BASE--ID"
            }
    """
    airtableconnect = json.load(open(filename))

    return airtableconnect


def airtableimport(baseid=None, apikey=None, configfile=None):
    """Import data from the airtable base.

        baseid : id of the base, string
        apikey : authentification key, string
        configfilename : path to a json config file

        Return a Library object
    """

    if configfile:
        info = connection(configfile)
        baseid = info['baseid']
        apikey = info['apikey']

    # connect to Airtable
    at = airtable.Airtable(baseid, apikey)

    # Download the tables
    print('download the tables :')
    materials_table = at.get('Materials')
    print(' get %i materials ' % len(materials_table['records']))

    properties_table = at.get('Properties')
    print(' get %i properties ' % len(properties_table['records']))

    values_table = at.get('Values')
    print(' get %i values ' % len(values_table['records']))

    # Create the Library
    library = ml.Library()

    # == import Properties ==
    # Add properties to the Library

    id2symbol_props = {}
    for record in properties_table['records']:

        symbol = record['fields']['Symbol']
        id2symbol_props[record['id']] = symbol

        prop = ml.Property(**record['fields'])  # create the Property Object
        library.addproperty(prop)

    print('%i physical properties added' % len(library.properties))

    # == import Values ==
    # populate a dict matid -> list of values

    def get_propertyobject(airtable_id):
        """ return the property object from the 'airtable' id
        """
        key = id2symbol_props[airtable_id]

        return library.properties[key]

    # Group values by material :
    sortedvalues = {}
    for valueinfo in values_table['records']:
        valueid = valueinfo['id']
        fields = valueinfo['fields']

        matid = fields['Material'][0]

        # Create the Value object
        value = ml.Value(value=fields['value'],
                         source=fields['Source'],
                         phiproperty=get_propertyobject(fields['Property'][0]))

        pytool.dictappend(sortedvalues, matid, value)

    # == import Materials ==
    for materialinfo in materials_table['records']:
        matid = materialinfo['id']
        fields = materialinfo['fields']

        # Create Material Object
        mat = ml.Material(name=fields['Name'],    # mandatory
                          values=sortedvalues.get(matid),
                          tags=fields.get('tags'),
                          chemicalcomp=fields.get('ChemicalComposition'))

        # Append the material to Library
        library.addmaterial(mat)

    return library
