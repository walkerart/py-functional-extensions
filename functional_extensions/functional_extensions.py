#test comment
def vformat(dictionary, *args, **kwargs):
    """
    Returns an new dictionary with its string values 
    formated with args and kwargs.
    It will drill down to find strings if dictionaries are nested.
    >>> vformat({'the': 'end{}'}, '?')
    {'the': 'end?'}
    >>> vformat({'the': 'beg{ex}'}, ex='!')
    {'the': 'beg!'}
    >>> vformat({'the': {'nested_dict': 'beggining{ex}'}}, ex='!')
    {'the': {'nested_dict': 'beggining!'}}
    >>> vformat({'the': True})
    {'the': True}
    """
    def typed_drill_down(v):
        return vformat(v, *args, **kwargs) if type(v) == dict else v
    def drill_down(v):
        return v.format(*args, **kwargs) if hasattr(v,'format') else typed_drill_down(v)
    return {k: drill_down(v) for k,v in dictionary.items()}

def uniq(strings):
    """
    Returns a list of strings passed through set
    >>> uniq(['k', 'k', 'j'])
    ['k', 'j']
    >>> uniq([{'what': 'other'}, {'what': 'other'}])
    Traceback (most recent call last):
    TypeError: unhashable type: 'dict'
    """
    return list(set(strings))

def exclude(keys, item):
    """
    Returns a new list excluding the keys passed in
    >>> exclude(['bad'], ['bad','good'])
    ['good']
    >>> exclude(['bad'], {'bad': False, 'good': True})
    {'good': True}
    """
    if type(item) == dict:
        ok_keys = [key for key in item.keys() if key not in keys]
        return only(ok_keys,item)
    elif iter(item):
        return [f for f in item if f not in keys]
    else:
        raise Exception('unable to handle type {}'.format(type(item)))

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
    {'end': 2}
    >>> only(['infinity'], {'start': 0, 'middle': 1, 'end': 2})
    {}
    """
    return {k: dictionary[k] for k in keys if k in dictionary.keys()}

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