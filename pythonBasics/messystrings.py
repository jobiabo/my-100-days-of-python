def repairsmessstr(string):
    spaced = " ".split(string)
    print(type(string))
    print(type(spaced))
    print(len(spaced))
    print(f"old string: {string}")
    for x in spaced:
        print(f"i found:", x)

repairsmessstr(" Hello WORLD ")