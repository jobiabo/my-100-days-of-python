import random
from menu import menupage
from userinput_validate import validate
from rangeint import inrangenumber
from board import guess

menupage()

rangednumber = input("Please enter end range: ")
rangedint = (inrangenumber(rangednumber))
print(f"rangedint: {rangedint}")

if rangedint == None:
    print("Range input is Null")
    exit()
else:
    rangedint = int(rangedint)
    cpu_guess = random.randint(1, (rangedint))




maxguess = 3
count = 1

while count <= 3:
    player_guess = (input("Enter your guess here: "))

    if validate(player_guess):
            guess(player_guess, cpu_guess)
            break

    if not validate(player_guess) and count < 3:
        print(f"you have used {count} trials, remaining {maxguess-count} trials")

    elif not validate(player_guess) and count == 3:
        print(f"You have given {count} wrong inputs")
        print("You failed")
        print("Computer won")
        break
    
    count=count+1
