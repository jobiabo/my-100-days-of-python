def guess(my_guess, cpu_guess):
    count = 1

    

    while my_guess != cpu_guess and count <= 5:
        
        my_guess = int(my_guess)
        if count > 1:
            my_guess = int(input("Enter your guess here: "))
        # trial 1
        if my_guess > cpu_guess and count == 1:
            
            print(f"not the number: {my_guess} too high")
            print(f"you have used {count} trial: {5-count} trials remaining")
            
        elif my_guess < cpu_guess and count == 1:
        
            print(f"not the number: {my_guess} too low")
            print(f"you have used {count} trial: {5-count} trials remaining")
        
        # trial 2
        elif my_guess > cpu_guess and count == 2:
            
            print(f"not the number: {my_guess} too high")
            print(f"you have used {count} trial: {5-count} trials remaining")
            
        elif my_guess < cpu_guess and count == 2:
        
            print(f"not the number: {my_guess} too low")
            print(f"you have used {count} trial: {5-count} trials remaining")
        # trial 3
        elif my_guess > cpu_guess and count == 3:
            
            print(f"not the number: {my_guess} too high")
            print(f"you have used {count} trial: {5-count} trials remaining")
            
        elif my_guess < cpu_guess and count == 3:
        
            print(f"not the number: {my_guess} too low")
            print(f"you have used {count} trial: {5-count} trials remaining")
        # trial 4
        elif my_guess > cpu_guess and count == 4:
            print(count)
            
            print(f"not the number: {my_guess} too high")
            print(f"you have used {count} trial: {5-count} trials remaining")
                
        elif my_guess < cpu_guess and count == 4:
            print(count)
        
            print(f"not the number: {my_guess} too low")
            print(f"you have used {count} trial: {5-count} trials remaining")
        
        # trial 5
        elif my_guess > cpu_guess and count == 5:
            
            print(f"not the number: {my_guess} too high")
            print(f"you have used {count} trial: 0 trials remaining")
            print("You failed")
            print("Computer Won!")
            break
            
        elif my_guess < cpu_guess and count == 5:
        
            print(f"Not the number: {my_guess} too low")
            print(f"You have used {count} trial: 0 trials remaining")
            print("You failed")
            print("Computer Won!")
            print(f"Computer secret number is {cpu_guess}")
            break   

        # Winning threshold
        if my_guess == cpu_guess:
            print(f"yay you got the number {cpu_guess}")
            print("You Won!")
            break
        count = count+1    
        


