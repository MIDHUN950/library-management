import os
from flask import Flask, request
import firebase_admin
from firebase_admin import auth, credentials, firestore
import base64
import imghdr
import uuid
import requests
import json
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
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.args["email"]
        password = request.args['password']
        URL = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyCSAoW2d9EYXO4QjgAGnR4H6bZuASM8d20"
        PARAMS = {
                'email':email,
                'password':password,
                'returnSecureToken': "true"
        }
        r = requests.post(url = URL, params = PARAMS)
        res = json.loads(r.text)
        if(r.status_code == 200):
            return {
                    "token": res["idToken"]
                }
        else:
            return res

@app.route('/take', methods = ["POST","GET"])
def take():
    if request.method == 'POST':
        token = request.headers["token"]
        bookName = request.args["bookName"]
        documents = [d for d in db.collection(u'Booth').where(u'bookId',u"==",bookName).stream()]
        if len(documents):
            return {
                    "error": "Book already taken"
                }
        documents = [d for d in db.collection(u'Books').where(u'bookId',u"==",bookName).stream()]
        if len(documents):
            return {
                    "error": "Book already exists"
                }

@app.route('/addBook', methods = ["POST","GET"])
def addBook():
    if request.method == "POST":
        token = request.headers["token"]
        title = request.args["title"]
        author = request.args["author"]
        description = request.args["description"]
        ti = str(title).upper().replace(" ","")
        au = str(author).upper().replace(" ","")
        documents = [d for d in db.collection(u'Books').where(u'bookId',u"==",ti+au).stream()]
        if len(documents):
            return {
                    "error": "Book already exists"
                }
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        # image = request.files["image"]
        # if imghdr.what(image) not in ["jpeg", "jpg","png"]:
        #     return "Invalid image format"
        # bid = str(uuid.uuid4())[:8]
        bid = ti+au
        data = {
            "title": title,
            "author": author,
            "description": description,
            "status": "available",
            "uid": uid,
            "bookId": bid,
            "createdAt": firestore.SERVER_TIMESTAMP
        }
        db.collection(u'Books').add(data)
        return "Added book to the shelf"

@app.route('/register', methods = ['POST',"GET"])
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
            regNo = str(request.args["regNo"]).upper()
            idCard = request.files['img']
            if imghdr.what(idCard) not in ["jpeg", "jpg","png"]:
                return "Invalid image format"
            b64 = base64.b64encode(idCard.read())
            if ((len(b64) * 3) / 4) > 1048000:
                return "Image size is longer than 1MB"
            data = {
                'email': email,
                'password': password,
                'firstname': firstname,
                'lastname': lastname,
                'imgB64': b64,
                'regNo': regNo,
                'limit': 3,
                'createdAt': firestore.SERVER_TIMESTAMP
            }
            URL = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyCSAoW2d9EYXO4QjgAGnR4H6bZuASM8d20"
            PARAMS = {
                'email':email,
                'password':password,
                'displayName':firstname+" "+lastname,
                'returnSecureToken': "true"
            }
            r = requests.post(url = URL, params = PARAMS)
            res = json.loads(r.text)
            if(r.status_code == 200):
                # user = auth.create_user(
                #     email= email,
                #     email_verified=False,
                #     password=password,
                #     display_name=firstname+" "+lastname)
                uid = res['localId']
                db.collection(u'Users').document(uid).set(data)
                return {
                    "token": res["idToken"]
                }
            else:
                return res
        except Exception as e:
            return str(e)