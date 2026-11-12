from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/temperature", methods=["GET", "POST"])
def age():

    if request.method == "POST":

        temp_value = request.form.get("celcius")
        if not temp_value:
            return "temperature value must not be empty"

        try:
            temp_value = float(temp_value)
            ferenheit = (temp_value*9/5)+32

            return f"{temp_value} in celcius is {ferenheit} in ferenheit"

        except ValueError:
            return "Please enter a valid temperatue"

    return render_template("temp.html")

if __name__ == "__main__":
    app.run(debug=True)