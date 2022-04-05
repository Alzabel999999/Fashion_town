from itertools import groupby


def group_list_of_dicts_by_key(dicts_list, key):
    keyfunc = lambda x: x[key]
    result = {k: list(v) for k, v in groupby(sorted(dicts_list, key=keyfunc), key=keyfunc)}
    return result
