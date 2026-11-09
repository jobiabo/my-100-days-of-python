from flask import Flask, render_template, request

app = Flask(__name__)
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("index.html")

    elif request.method == "POST":
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        country = request.form.get("country")

        return f"""
            <h1>Registration Successful!</h1>
            <p>Name: {fullname}</p>
            <p>Email: {email}</p>
            <p>Country: {country}</p>
        """

if __name__ == "__main__":
    app.run(debug=True)