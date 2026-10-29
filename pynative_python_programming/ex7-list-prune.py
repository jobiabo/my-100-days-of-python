def cart(select):
    select.append("mango")
    select.pop(select[1])
    print(select)


fruits = ["apple", "banana", "cherry", "date", "elderberry"]
cart(fruits)
