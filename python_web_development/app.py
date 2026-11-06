from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    print("I came first")
    return "<h1>I come second</h1>"

@app.route("/about")
def about():
    return "<h1>ABOUT US</h1>"

@app.route("/whoami")
def mypeace():
    return "<h1>Jehovah My Decorator</h1>"

if __name__ == "__main__":
    app.run(debug=True)