from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return "<h1>This is a GET request"
    elif request.method == "POST":
        return "<h1>This is a POST request"

@app.route("/about")
def about():
    return "<h1>ABOUT US</h1>"

@app.route("/whoami")
def mypeace():
    return "<h1>Jehovah My Decorator</h1>"

if __name__ == "__main__":
    app.run(debug=True)