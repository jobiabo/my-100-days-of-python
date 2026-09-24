entry = input("Enter score here: ")
score = int(entry)

match score:
    case _ if score > 100 or score < 0:
        print("Please enter a valid score")
    case _ if score >= 80:
        print(f"{score} is Grade A")
    case _ if score >= 75:
        print(f"{score} is Grade B")
    case _ if score >= 50:
        print(f"{score} is Grade C")
    case _ if score >= 40:
        print(f"{score} is Grade D")
    case _ if range(0, 40):  # Alternative way to check a strict range
        print(f"{score} is Grade F")
