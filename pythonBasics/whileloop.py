# entry = input("enter text here: ")
entry = "the man bought a apple"
split = entry.split(" ")
print(entry, type(entry))
print(split, type(split))

i = 0 
while i < len(split):
    if split[i][0] == "a" or "e" or "i" or "o" or "u" and i > 1:
        print(split[i][0])
        if split[i-1] == "a":
            print(split[i-1])
            split[i-1] = "an"
    i = i+1
print(split)
cleaned = " ".join(split)
print("cleaned;", cleaned)

# for x in split:
#     print(x)
    
# print(split)    