def cart(select):
    select.append("mango")
    select.remove(select[1])
    print(select)


fruits = ["apple", "banana", "cherry", "date", "elderberry"]
cart(fruits)
