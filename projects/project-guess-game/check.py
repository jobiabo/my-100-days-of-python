# import random

# def guess(x):
#     cpu_random = random.randint(1, x)

#     count = 1

#     while count <= 5:
#         my_guess = int(input("Guess a number: "))

#         if my_guess == cpu_random:
#             print(f"Yay! You got the number {cpu_random}")
#             print("You Won!")
#             break

#         elif my_guess > cpu_random:
#             print(f"Not the number: {my_guess}, too high")

#         else:
#             print(f"Not the number: {my_guess}, too low")

#         print(f"You have used {count} trial(s): {5-count} trials remaining")

#         if count == 5:
#             print("You failed")
#             print("Computer Won!")
#             break

#         count += 1


# guess(5)




def validate():
    i = 1
    while i <= 3:
        user_input = input("enter a number: ")
        if user_input.isdigit():
            return True
        
        if i == 3:
            print("You failed!, unable to provide valid input")
            break
        i+=1
  
            
validate()




