from flask import Flask, request

app = Flask(__name__)

@app.route("/register", methods=["POST"])
def register():

    username = request.form.get("username")
    if not username:
        return "Username is required", 400
    return "User registered successfully", 201

   

if __name__ == "__main__":
    app.run(debug=True)