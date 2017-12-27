


def dictappend( dico, key, value ):
    """ append 'value' to the list dico[key] or create the list [value, ]
    """
    if key in dico:
        dico[key].append( value )
    else:
        dico[key] = [value, ]
