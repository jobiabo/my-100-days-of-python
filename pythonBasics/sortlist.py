thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist.sort()
print(thislist)
alphabets = ["q", "m", "a", "z", "f", "t", "b", "x", "h", "r", "k", "w", "c", "y", "n", "d", "u", "j", "p", "g", "v", "e", "s", "l", "o", "i"]
newlist = ["q", "m", "a", "z", "f", "t", "b", "x", "h", "r", "k", "w", "c", "y", "n", "d", "u", "j", "p", "g", "v", "e", "s", "l", "o", "i"]
newlist.sort()

# python preserve a kinda identity var memory preservation when it comes to manipulations
# when it comes on when i did newlist = alphabet, then sorted newlist, alphabet was also sorted.
print("alphabets =", alphabets)
print("new sorted list =", newlist)