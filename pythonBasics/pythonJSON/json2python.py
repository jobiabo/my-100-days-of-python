import json

with open("student.json", "r") as file:
    student = json.load(file)
    print(student["name"])
    print(f"{student}\nis datatype {type(student)}")
    student["is_student"] = True
    print(student)


with open("student.json", "w") as file:
    json.dump(student, file, indent=4)
    print("file written successsfully")