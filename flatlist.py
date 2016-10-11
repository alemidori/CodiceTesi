
def flat(inputlist):
    list = []
    flatten = lambda l: sum(map(flatten, l), []) if isinstance(l, list) else [l]
    list = flatten(inputlist)
    return list
