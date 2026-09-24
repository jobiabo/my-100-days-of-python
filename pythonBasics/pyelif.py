print("Enter score here:")
entry = input()
score = int(entry)
if score >100:
    print("please enter valid score")
elif score >= 80:
    print(f"{score} is Grade A")
elif score >= 75:
    print(f"{score} is Grade B")
elif score >= 50:
    print(f"{score} is Grade C")
elif score >= 40:
    print(f"{score} is Grade D")
elif score >= 40:
    print(f"{score} is Grade E")
elif score < 40:
    print(f"{score} is Grade F")
