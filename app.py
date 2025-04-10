from flask import Flask, request
from flask_cors import CORS
import requests #for downlaoding data image
import smtplib #for sending email
import os #for env key
from dotenv import load_dotenv



app = Flask(__name__)
CORS(app)


load_dotenv() #get all the data in .env

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

image_test = None


@app.route('/')
def home():
    global image_test

    if image_test:
        return f"<h2>Last image sent:</h2> <img src='{image_test}' style='max-width:600px;'>"
    else:
        return "<p>No image sent yet.</p>"


#when someone ask for request to/send using post method, run the function below
@app.route("/send", methods=["POST"])
def send(): 
    global image_test


    data = request.json  
    email_to = data["email"]
    subject = data["subject"]
    image_url = data["imageUrl"]

    image_test = image_test

    #brevo expected format
    email_data = {
        #sender should be like dict
        "sender": {
            "name": "Random image for you!",
            "email": SENDER_EMAIL
        },

        #to should be array
        "to": [
            {
                "email": email_to
            }
        ],

        #subject is string
        "subject": subject,

        #can be a string, but since we are passing image_url variable, need to put f infront
        "htmlContent": f"""
            <html>
                <body>
                    <h1>HAHAHAHAHAHA</h1>
                    <img src="{image_url}" style="max-width:600px;">
                </body>
            </html>
        """
    }

    #u post request to api, asking if you can send a data,.
    response = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        #include api key, and telling the content type, and accept type
        headers={
            "api-key": BREVO_API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        #you are sending email_data in json, if u do json=smt, its gonna change it into json format
        json=email_data
    )


    print("Email sent response:", response.status_code, response.text)

    return "Email sent!", 200





if __name__ == "__main__":
    app.run(debug=True)
    print("heellooo")
