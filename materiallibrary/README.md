# Material library
A python interface to access and use database of physical properties of materials.

The database currently used is airtable.com, which provides online relational like database easily editable.

The datebase should be structured using 3 tables as follow :

```
Table Materials
===============
    Name (string), unique
    [tags] (list of string)
    [ChemicalFormula] (string)

Table Values
============
    id, unique
    material_id
    property_id
    value (float)
    [source] (string)

Table Properties
================
    symbol (string), unique
    unit (string)
```

- A material could have multiple values for the same property. The values can be accessed using for example the `_min`, `_max` or `_array` suffix.


## Usage
```python
from materiallibrary import airtableimport
library = airtableimport( configfile='airtable-connection.json' )

cuivre = library.materials['Cuivre']
cuivre.k  # thermal conductivity
>>> 380.0
```


```python

cuivre = library.materials['Cuivre']

```


## Work in progress

Secondary properties:
- defined using material properties
- can also be defined directly


## What for ?
### for simulation

```python
mat = lib.materials( 'Mat' )
res = Simu( mat )
```

```python
mat1, mat2 = lib.materials( 'Mat' ), ...
res = Simu( mat1, mat2 )
```

Avec toutes les combinaisons min/max des props. possible?
```python
mat = lib.materials( 'Mat' )
allres = Simu_all( mat )

simu_all.props
```

### For material selection

```python
Ashby_plot( materials.rho, materials.E )
```
