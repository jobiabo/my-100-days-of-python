def fact(number):
    brack = []
    product = 1
    i = 1
    while i <= number:
        brack.append(i)
        i = i+1
    for x in brack:
        product = product*x
    return product

print(fact(6))



# optimized 
'''
def fact(number):
    product = 1
    i = 1

    while i <= number:
        product *= i
        i += 1

    return product

print(fact(6))  # 720
'''