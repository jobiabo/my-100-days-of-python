
listofnum = []
i = 0
while i <= 10:
    listofnum.append(i)
    print(i)
    i=i+1
print("total =", listofnum)   

total = 0
for x in listofnum:
    total += listofnum[x]
print(total)

