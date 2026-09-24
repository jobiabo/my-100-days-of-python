def isArticle(text):
    split = text.split(" ")
   

    for ind, val in enumerate(split):
        if ind >0 and val[0] == "a"  and split[ind-1] == "a":
            print(split[ind-1])
            split[ind-1] = "an"
        elif val[0] == "e":
            print(split[ind-1])
            split[ind-1] = "an"
        elif val[0] == "i":
            print(split[ind-1])
            split[ind-1] = "an"
        elif val[0] == "o":
            print(split[ind-1])
            split[ind-1] = "an"
        elif val[0] == "u":
            print(split[ind-1])
            split[ind-1] = "an"
    return split
               
    


