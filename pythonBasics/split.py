a = "The man the how a car"
g = a.split(" ")
print(g)

for x in g:
    if "the" in g:
        print(f"{x}")

#this part joins the splitted list
d = g
e = " ".join(d)
print(e)