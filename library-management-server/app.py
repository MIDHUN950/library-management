import os
from flask import Flask, request
import firebase_admin
from firebase_admin import auth, credentials, firestore
import base64
import imghdr

cred = credentials.Certificate('library-management-web-firebase-adminsdk-ejrkp-1aff66da09.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

@app.route('/', methods = ['POST',"GET"])
def welcome():
    return "<h1>Library Management API</h1>"
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/login', methods = ["GET"])
def login():
    if request.method == "GET":
        
        return "<h1>Login</h1>"

@app.route('/register', methods = ['POST'])
def register():
    """
    This is the route of the Flask application.
    It is called when the user submits the registration form.
    """
    if request.method == 'POST':
        try:
            email = request.args['email']
            password = request.args['password']
            firstname = request.args['firstname']
            lastname = request.args['lastname']
            regNo = request.args["regNo"]
            idCard = request.files['img']
            if imghdr.what(idCard) not in ["jpeg", "jpg","png"]:
                return "Invalid image format"
            data = {
                'email': email,
                'password': password,
                'firstname': firstname,
                'lastname': lastname,
                'imgB64': base64.b64encode(idCard.read()),
                'regNo': regNo,
                'limit': 3
            }
            user = auth.create_user(
                email= email,
                email_verified=False,
                password=password,
                display_name=firstname+" "+lastname)
            uid = user.uid
            c_token = auth.create_custom_token(uid)
            db.collection(u'Users').document(user.uid).set(data)
            res = {
                "token": c_token
            }
            return res
        except Exception as e:
            return str(e)