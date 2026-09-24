data = {
    "name": "john",
    "class": "200lv",
    "sex": "male"
}
print(data)
print("\n")


# for x in data:
#     print(data[x])

#looping through dict using the key() to access the key
for key in data.keys():
    print(key)
    
print("\n")
#looping through dict using the values() to access the values
for value in data.values():
    print(value)
print("\n")

#looping through dict using the item() to print both key and vale

for x, y in data.items():
    print(x, y)