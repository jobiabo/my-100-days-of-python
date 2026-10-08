from userinput_validate import validate

def inrangenumber(rangednumber):
    if validate(rangednumber):
        return rangednumber
    else:
        print("please enter a valid integer from 0 upward")
        return