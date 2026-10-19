from taskservice import create_task
from taskservice import view_all_tasks
from modified import mark_complete
from modified import mark_incomplete
from config import heading
import sys

def main():

    while True:
        heading()

        try:
            choice = input("Enter option: ")

            if choice == "1":
                view_all_tasks()
            elif choice == "2":
                title = input("Enter Task title: ")
                if title == "":
                    print("Title cannot be empty")
                    title = input("Enter Task title")
                    create_task(title)

                else:
                    create_task(title)
            elif choice == "3":
                mark_complete()
            elif choice == "4":
                mark_incomplete()
            elif choice == "0":
                print("GOODBYE")
                return
            else:
                print("Enter valid option")
        except KeyboardInterrupt:
            print("\n\n[!] Interruption detected. Safely exiting menu...")
            sys.exit(0)



            



main()
# mark_complete()
# print(MENU)
# create_task(title)
# view_all_tasks()

