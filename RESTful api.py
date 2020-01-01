################################ IMPORTS #######################################
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_mongoengine import MongoEngine, Document

################################# CONFIGURATIONS ###############################################
app = Flask(__name__)
CORS(app)
app.secret_key = "myapplicationsecretkeygoeshere"
app.config['MONGO_URI'] = "mongodb://localhost:27017/CollectionName"
mongo = PyMongo(app)

################################ ROUTES ########################################################
#for Logging in
@app.route('/login', methods=['POST'])
def login_user():
    _json = request.json
    _email = _json['email']
    _password = _json['password']

    if _email and _password and request.method == 'POST':
        user = mongo.db.user.find_one({'email': str(_email)})
        _hashed_password = generate_password_hash(_password)
        if(user):
            if check_password_hash(user['password'], _password):
                resp = jsonify("Found")
                resp.status_code = 200
                return resp
        else:
            return not_found()
    else:
        return not_found()

##Registering user
@app.route('/adduser', methods=['POST'])
def add_user():
    _json = request.json
    _firstname = _json['firstname']
    _lastname = _json['lastname']
    _email = _json['email']
    _password = _json['password']
    _contact = _json['contact']
    

    print(_json)

    if _firstname and _lastname and _email and _password and _contact and request.method == 'POST':

        _hashed_password = generate_password_hash(_password)
        id = mongo.db.user.insert_one(
            {'firstname': _firstname, 'lastname': _lastname,
             'email': _email, 'password': _hashed_password, 'contact': _contact}
        )

        resp = jsonify("Added successfully")

        resp.status_code = 200

        return resp

    else:
        return not_found()
#getting all users from db
@app.route('/getusers')
def users():
    users = mongo.db.user.find()
    resp = dumps(users)

    return resp

#getting user with specific id
@app.route('/user/<id>')
def user(id):
    user = mongo.db.user.find_one({'_id': ObjectId(id)})
    resp = dumps(user)
    return resp

#deleting user with specific id
@app.route('/delete/<id>', methods=["'DELETE'"])
def delete_user(id):
    mongo.db.user.delete_one({'_id': ObjectId(id)})
    resp = jsonify('User deleted successfully!')
    resp.status_code = 200
    return resp

#updating user with specific id
@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    _id = id
    _json = request.json
    _firstname = _json['firstname']
    _lastname = _json['lastname']
    _email = _json['email']
    _password = _json['password']
    _contact = _json['contact']

    if _id and _firstname and _lastname and _email and _password and request.method == "PUT":
        _hashed_password = generate_password_hash(_password)
        mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(
            _id)},
            {'$set': {'firstname': _firstname, 'lastname': _lastname, 'email': _email, 'password': _hashed_password,'contact': _contact}})

        resp = jsonify("User Updated Successfully")
        resp.status_code = 200
        return resp

    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404, 'message': 'Not Found '+request.url
    }
    resp = jsonify(message)

    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run(debug=True)
