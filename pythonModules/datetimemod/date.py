import datetime

def clock():
    now = datetime.datetime.now()
    rawtime = f"The  time is {datetime.datetime.now()}"

    onlytime = now.strftime("%p")
    return rawtime, onlytime


print(clock())