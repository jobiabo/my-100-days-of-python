from userinput_validate import validate
def guess(player_guess, cpu_guess):
    count = 1

    

    while player_guess != cpu_guess and count <= 5:        
        player_guess = int(player_guess)        

        if count > 1:
            player_guess = (input("Enter your guess here: "))
            if not validate(player_guess):
                print(f"Your guess is invalid you failed, {player_guess} is not a valid integer")
                print(f"Computer won! with {cpu_guess} as secret number")

                break
            else:
                player_guess = int(player_guess)

            

        # trial 1
        if player_guess > cpu_guess and count == 1:
            
            print(f"not the number: {player_guess} too high")
            print(f"you have used {count} trial: {5-count} trials remaining")
            
        elif player_guess < cpu_guess and count == 1:
        
            print(f"not the number: {player_guess} too low")
            print(f"you have used {count} trial: {5-count} trials remaining")
        
        # trial 2
        elif player_guess > cpu_guess and count == 2:
            
            print(f"not the number: {player_guess} too high")
            print(f"you have used {count} trial: {5-count} trials remaining")
            
        elif player_guess < cpu_guess and count == 2:
        
            print(f"not the number: {player_guess} too low")
            print(f"you have used {count} trial: {5-count} trials remaining")
        # trial 3
        elif player_guess > cpu_guess and count == 3:
            
            print(f"not the number: {player_guess} too high")
            print(f"you have used {count} trial: {5-count} trials remaining")
            
        elif player_guess < cpu_guess and count == 3:
        
            print(f"not the number: {player_guess} too low")
            print(f"you have used {count} trial: {5-count} trials remaining")
        # trial 4
        elif player_guess > cpu_guess and count == 4:
            print(count)
            
            print(f"not the number: {player_guess} too high")
            print(f"you have used {count} trial: {5-count} trials remaining")
                
        elif player_guess < cpu_guess and count == 4:
            print(count)
        
            print(f"not the number: {player_guess} too low")
            print(f"you have used {count} trial: {5-count} trials remaining")
        
        # trial 5
        elif player_guess > cpu_guess and count == 5:
            
            print(f"not the number: {player_guess} too high")
            print(f"you have used {count} trial: 0 trials remaining")
            print("You failed")
            print("Computer Won!")
            break
            
        elif player_guess < cpu_guess and count == 5:
        
            print(f"Not the number: {player_guess} too low")
            print(f"You have used {count} trial: 0 trials remaining")
            print("You failed")
            print("Computer Won!")
            print(f"Computer secret number is {cpu_guess}")
            break   

        # Winning threshold
        if player_guess == cpu_guess:
            print(f"yay you got the number {cpu_guess}")
            print("You Won!")
            break
        
        count = count+1    
        


