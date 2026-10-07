import random
from my_uservalidate import validate
from errorMess import error_Message

def guess(x):
    count = 1

    while count < 10:
        cpu_random = random.randint(1, x)
        my_guess = 0

        while my_guess != cpu_random and count <= 5:
            my_guess = (input("guess a number: "))
            if validate(my_guess):
                my_guess = int(my_guess)
                # trial 1
                if my_guess > cpu_random and count == 1:
                    
                    print(f"not the number: {my_guess} too high")
                    print(f"you have used {count} trial: {5-count} trials remaining")
                    
                elif my_guess < cpu_random and count == 1:
                
                    print(f"not the number: {my_guess} too low")
                    print(f"you have used {count} trial: {5-count} trials remaining")
                # trial 2
                elif my_guess > cpu_random and count == 2:
                    
                    print(f"not the number: {my_guess} too high")
                    print(f"you have used {count} trial: {5-count} trials remaining")
                    
                elif my_guess < cpu_random and count == 2:
                
                    print(f"not the number: {my_guess} too low")
                    print(f"you have used {count} trial: {5-count} trials remaining")
                # trial 3
                elif my_guess > cpu_random and count == 3:
                    
                    print(f"not the number: {my_guess} too high")
                    print(f"you have used {count} trial: {5-count} trials remaining")
                    
                elif my_guess < cpu_random and count == 3:
                
                    print(f"not the number: {my_guess} too low")
                    print(f"you have used {count} trial: {5-count} trials remaining")
                # trial 4
                elif my_guess > cpu_random and count == 4:
                    print(count)
                    
                    print(f"not the number: {my_guess} too high")
                    print(f"you have used {count} trial: {5-count} trials remaining")
                    
                elif my_guess < cpu_random and count == 4:
                    print(count)
                
                    print(f"not the number: {my_guess} too low")
                    print(f"you have used {count} trial: {5-count} trials remaining")
                
                # trial 5
                elif my_guess > cpu_random and count == 5:
                    
                    print(f"not the number: {my_guess} too high")
                    print(f"you have used {count} trial: 0 trials remaining")
                    print("You failed")
                    print("Computer Won!")
                    break
                    
                elif my_guess < cpu_random and count == 5:
                
                    print(f"Not the number: {my_guess} too low")
                    print(f"You have used {count} trial: 0 trials remaining")
                    print("You failed")
                    print("Computer Won!")
                    break
    
                # Winning threshold
                else:
                    print(f"yay you got the number {cpu_random}")
                    print("You Won!")
                count = count+1

            elif not validate(my_guess) and count == 3:
                print("You failed, after 3 invalid input trials ")  
            else:
                print(error_Message())
                break

        break




guess(5)