def divide():
    from functools import reduce
    import operator
    mylist = [10, 5, 2, 8, 0]
    # Calculates 10 / 5
    total = reduce(operator.truediv, mylist)
    return total
print(divide())