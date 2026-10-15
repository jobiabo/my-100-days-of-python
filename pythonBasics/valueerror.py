def checkerror():
    try:
        mathh = 10/0
        # print(mathh)
        # raise ValueError
    except:
        # print("i raised an error")
        print("math incomplete")

checkerror()