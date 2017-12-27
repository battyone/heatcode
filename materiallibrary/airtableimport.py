# coding: utf-8

# -- import from the airtable database --
#  https://airtable.com/


#     Database specification
#     ---------------------
#
#     Table Materials
#         Name (string), unique
#         [tags] (list of string)
#         [ChemicalFormula] (string)
#
#     Table Values
#         id
#         material_id
#         property_id
#         value (float)
#         [source] (string)
#
#     Table Properties
#         symbol (string), unique
#         unit (string)
#

from . import materiallibrary as ml
from . import pythontools as pytool

import json
from airtable import airtable
# https://github.com/nicocanali/airtable-python
# https://github.com/nicocanali/airtable-python/issues/10

def connection():
    """ get the api-key and database id (see in the api help example) from
        the configuration file (json):
            {
            "apikey":"MY--KEY",
            "baseid":"MY--BASE--ID"
            }
        return an AirTable connection object
    """
    airtableconnect = json.load( open('airtable-connection.json') )
    at = airtable.Airtable(airtableconnect['baseid'], airtableconnect['apikey'])
    return at

def airtableimport():
    """ import data from the airtable base
        return a Library object
    """

    at = connection()  # to clean ..

    # Download the tables
    materials_table = at.get('Materials')
    properties_table = at.get('Properties')
    values_table = at.get('Values')



    # Create the Library
    library = ml.Library()



    # == import Properties ==
    # Add properties to the Library

    id2symbol_props = {}
    for record in properties_table['records']:

        symbol = record['fields']['Symbol']
        id2symbol_props[ record['id'] ] = symbol

        prop = ml.Property( **record['fields'] )  # create the Property Object
        library.addproperty( prop )

    print( '%i physical properties added' % len(library.properties) )



    # == import Values ==
    # populate a dict matid -> list of values

    def get_propertyobject( airtable_id ):
        """ return the property object from the 'airtable' id
        """
        key = id2symbol_props[airtable_id]
        return library.properties[ key ]


    # group values by material
    sortedvalues = {}
    for valueinfo in values_table['records']:
        valueid = valueinfo['id']
        fields = valueinfo['fields']

        matid = fields['Material'][0]

        # create the Value object
        value = ml.Value( value=fields['value'],
                                       source=fields['Source'],
                                       phiproperty=get_propertyobject( fields['Property'][0] )
                                     )

        pytool.dictappend( sortedvalues, matid, value )



    # == import Materials ==
    for materialinfo in materials_table['records']:
        matid = materialinfo['id']
        fields = materialinfo['fields']

        # create Material Object
        mat = ml.Material( name=fields['Name'], # mandatory
                           values=sortedvalues.get( matid ),
                           tags=fields.get( 'tags' ),
                           chemicalcomp=fields.get( 'ChemicalComposition' ) )

        # Append the material to Library
        library.addmaterial( mat )


    return library
