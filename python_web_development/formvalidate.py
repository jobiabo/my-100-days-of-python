from flask import Flask, request

app = Flask(__name__)

@app.route("/age", methods=["GET", "POST"])
def age():

    if request.method == "POST":

        user_age = request.form.get("age")

        try:
            user_age = int(user_age)

            return f"Your age is {user_age}"

        except ValueError:
            return "Please enter a valid age"

    return "Age Form"