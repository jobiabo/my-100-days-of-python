def fact(number):
    brack = []
    product = 1
    i = 1
    while i <= number:
        if i <= number:
            brack.append(i)
            i = i+1
    for x in brack:
        product = product*x
    return product

print(fact(6))