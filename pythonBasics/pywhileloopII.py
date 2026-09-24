# entry = input("enter text here: ")
entry = "the man bought a apple"
split = entry.split(" ")
print(entry, type(entry))
print(split, type(split))

for ind, val in enumerate(split):
    if val[0] == "a" and split[ind-1] == "a":
      split[ind-1] = "an"
      print(split[ind-1])


    
print(split)  

print(split)
cleaned = " ".join(split)
print("cleaned;", cleaned)

  