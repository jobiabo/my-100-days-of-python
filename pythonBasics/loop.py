mylist = ("bmw", "volvo", "mercedes", "toyota")
for x in mylist:
    if x == "toyota":
        print(f"{x} found at", mylist.index(x))