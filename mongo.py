from flask import Flask, jsonify, request, jsonify, make_response
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from gridfs import GridFS
from pymongo import MongoClient


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://itsme:itsme@cluster0-e7bn4.mongodb.net/test?retryWrites=true&w=majority"

mongo = PyMongo(app)

app.config['JWT_SECRET_KEY'] = 'secret'

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

MONGO_CLIENT = MongoClient('mongodb+srv://itsme:itsme@cluster0-e7bn4.mongodb.net/test?retryWrites=true&w=majority')
DB = MONGO_CLIENT['files']
GRID_FS = GridFS(DB)

CORS(app)

@app.route('/users/upload', methods=['GET','POST'])
def uploadFile():
    with GRID_FS.new_file(filename=request.files['file'].filename) as fp:
        fp.write(request.files['file'])
        file_id = fp._id
    if GRID_FS.find_one(file_id) is not None:
        return 'Image Upload Successfully'
    else:
        response.status = 500
        return 'Error occurred while saving file.'

@app.route('/users/download', methods=['GET', 'POST'])
def index():
    grid_fs_file = GRID_FS.find_one({'filename': request.args.get('file_name')})
    response = make_response(grid_fs_file.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers["Content-Disposition"] = "attachment; filename={}".format(request.args.get('file_name'))
    return response

@app.route('/users/updateDate', methods=['POST'])
def updateDate():
    mongo.db.users.find_one_and_update(
        {"username" : request.get_json()['username']},
        {"$set": {"file_name": request.get_json()['file_name']}},
        upsert = True
    )
    return 'add'
    # update({"_id" :ObjectId("4e93037bbf6f1dd3a0a9541a") },{$set : {"new_field":1}})

@app.route('/users/checkUser', methods=['GET'])
def checkUser():
    users = mongo.db.users
    username = request.args.get('username')
    response = users.find_one({'username': username})
    if response:
        return "Exists"
    return "Free"

@app.route('/users/deleteFile', methods=['DELETE'])
def delFile():
    mongo.db.users.find_one_and_update(
        {"username" : request.args.get('username')},
        {"$set": {"file_name": ' '}},
        upsert = True
    )
    return 'delete'

@app.route('/users/register', methods=['POST'])
def register():
    users = mongo.db.users
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    username = request.get_json()['username']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    file_name = request.get_json()['file_name']
    created = datetime.utcnow()

    user_id = users.insert({
        'first_name': first_name,
        'last_name': last_name,
        'username': username,
        'email': email,
        'password': password,
        'file_name': file_name,
        'created': created
    })

    new_user = users.find_one({'_id': user_id})

    result = {'email': new_user['email'] + ' registered'}

    return jsonify({'result' : result})

@app.route('/users/login', methods=['POST'])
def login():
    users = mongo.db.users
    username = request.get_json()['username']
    password = request.get_json()['password']
    result = ""

    response = users.find_one({'username': username})

    if response:
        if bcrypt.check_password_hash(response['password'], password):
            access_token = create_access_token(identity = {
                'first_name': response['first_name'],
                'last_name': response['last_name'],
                'username': response['username'],
                'email': response['email'],
                'file_name': response['file_name']
            })
            result = jsonify({"token": access_token})
        else:
            result = jsonify({"error": "Invalid username and password"})
    else:
        result = jsonify({"result": "No results found"})
    return result

if __name__ == '__main__':
    app.run(debug=True)
