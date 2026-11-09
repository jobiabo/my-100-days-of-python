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

# Identifying Query Parameters
@app.route("/hello")
def hello():
    name = request.args.get("name")
    age = request.args.get("age")
    return f"<h1>Hello {name}!\n he is {age} years of age</h1>"

if __name__ == "__main__":
    app.run(debug=True)