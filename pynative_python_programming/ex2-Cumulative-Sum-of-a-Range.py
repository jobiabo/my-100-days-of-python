def loopiterate():
    numbers = range(10)
    print(numbers)
    i = 1
    while i < len(numbers):
        print(f"current numbers {numbers[i]}, previous number {numbers[i-1]}, sum {numbers[i]+numbers[i-1]}")
        i = i+1

loopiterate()