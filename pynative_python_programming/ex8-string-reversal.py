# def reverse(string):
#     i = len(string)-1
#     j = 0
#     final =""
#     while i <= len(string) and i >= j:
#         final = final+string[i]
#         i=i-1
#     return final

# print(reverse("python"))


# optimised 

def reverse(string):
    return string[::-1]

print(reverse("python"))
# nohtyp