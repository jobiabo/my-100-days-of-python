# def vowel_counter(string):
#     string = string.lower()
#     count = 0
#     for x in string:
#         if x == "a" or x == "e" or x == "i" or x == "o" or x == "u":
#             count +=1
#     return count


# sentence = "Learning Python is fun!"
# print(vowel_counter(sentence))

# Optimised 

def vowel_counter(string):
    string = string.lower()
    count = 0

    for x in string:
        if x in "aeiou":
            count += 1

    return count


sentence = "Learning Python is fun!"
print(vowel_counter(sentence))
# 6