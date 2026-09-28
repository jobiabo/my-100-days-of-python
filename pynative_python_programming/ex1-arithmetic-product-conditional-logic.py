def threshcheck(num1, num2):
    if num1 * num2 <= 1000:
        return num1*num2
    else:
        return num1+num2
        
print(threshcheck(20, 30))
print(threshcheck(40, 30))