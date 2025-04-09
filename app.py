from flask import Flask, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)




@app.route("/send", methods=["POST"])
def send():
    data = request.json  
    print("Received data:", data)

    return "OK", 200



if __name__ == "__main__":
    app.run(debug=True)
    print("heellooo")
