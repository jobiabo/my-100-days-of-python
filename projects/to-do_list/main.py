from taskservice import create_task
from taskservice import view_all_tasks
from modified import mark_complete

def main():
    title = input("Enter task title: ")
    create_task(title)

# main()
# view_all_tasks()
mark_complete()