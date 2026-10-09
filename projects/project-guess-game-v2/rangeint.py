from userinput_validate import validate

def inrangenumber(rangednumber):
    rangeinput = list(rangednumber)
    i = 0
    while i < len(rangeinput):
        if validate(rangednumber):
            return rangednumber
        else:
            print("please enter a valid integer from 0 upward")
            return None
    i=i+1