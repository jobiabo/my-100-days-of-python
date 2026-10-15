import datetime

def welcomedash(name):
    now = datetime.datetime.now()
    if now.strftime("%p") == "AM":
        return f"Good morning, {name}!"
    else:
        return f"Good afternoon, {name}!"


print(welcomedash("Joel"))