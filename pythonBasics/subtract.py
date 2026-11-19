def subtract():
    from functools import reduce
    import operator
    mylist = [10, 5, 2, 1, 9]
    # Calculates 10 - 5
    total = reduce(operator.sub, mylist)
    return total
print(subtract())