import random

def guess(x):
    count = 0

    while count < 5:
        cpu_random = random.randint(1, x)
        my_guess = 0

        while my_guess != cpu_random and count < 5:
            my_guess = int(input("guess a number: "))
            
            if my_guess > cpu_random and count == 5:
                print(f"not the number {my_guess} too high")
                print("you failed all your 5 trials")
                break
            elif my_guess < cpu_random and count == 5:
                print(f"not the number {my_guess} too low")
                print("you failed all your 5 trials")
                break
            elif my_guess > cpu_random:
                print(f"not the number {my_guess} too high")
            elif my_guess < cpu_random:
                print(f"not the number {my_guess} too low")                
            else:
                print(f"yay you got the number {cpu_random}")
            count = count+1
        break




guess(5)