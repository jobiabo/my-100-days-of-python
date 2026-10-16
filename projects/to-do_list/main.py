from taskservice import create_task
from taskservice import view_all_tasks

def main():
    title = input("Enter task title: ")
    create_task(title)

# main()
view_all_tasks()