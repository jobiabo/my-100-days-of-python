from flask import Flask, render_template, request

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("base.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("index.html")

    elif request.method == "POST":
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        country = request.form.get("country")

        return render_template(
            "result.html",
            fullname=fullname,
            email=email,
            country=country,
        )

if __name__ == "__main__":
    app.run(debug=True)