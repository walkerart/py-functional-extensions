def merge_with(func, *dictionaries):
    """
    Returns a map that consists of the rest of the maps conj-ed onto
    the first.  If a key occurs in more than one map, the mapping(s)
    from the latter (left-to-right) will be combined with the mapping in
    the result by calling (f val-in-result val-in-latter).
    >>> merge_with(min, {'k': 1}, {'k': 2}, {'k':3, 'y':'z'})
    {'y': 'z', 'k': 1}
    """
    dd = {}
    for d in dictionaries:
        for item in d.items():
            if item[0] in dd:
                dd[item[0]] = func(dd[item[0]], item[1])
            else:
                dd[item[0]] = item[1]
    return dd

def only(keys, dictionary):
    """ 
    Returns only the items from dictionary with keys in keys
    >>> only(['start','end'], {'start': 0, 'middle': 1, 'end': 2})
    {'start': 0, 'end': 2}
    >>> only(['infinity','end'], {'start': 0, 'middle': 1, 'end': 2})
    Traceback (most recent call last):
    KeyError: 'infinity'
    """
    return {k: dictionary[k] for k in keys}

def force_ints(dictionary):
    """
    Call int() on all values of dictionary
       >>> force_ints({'start': '0', 'end' : 2})
       {'start': 0, 'end': 2}
       >>> force_ints({'start': '0', 'end' : 'word' })
       Traceback (most recent call last):
       ValueError: invalid literal for int() with base 10: 'word'
    """
    return {key: int(val) for key,val in dictionary.items() }

def filter_none(dictionary):
    """
    Returns items in dictionary with a value other than None
    
       >>> filter_none({'start':0, 'middle': None}) 
       {'start': 0}
    """
    return dict(filter(lambda x: x[1] != None, dictionary.items()))


def update_if_none(dictionary, update):
    """
    Update or remove all items in dictionary with a value
        >>> update_if_none({'start': 0, 'middle': None}, {'start': 1, 'middle': 2})
        {'start': 0, 'middle': 2}
    """
    update.update(filter_none(dictionary))
    return update

if __name__ == "__main__":
    import doctest
    doctest.testmod()