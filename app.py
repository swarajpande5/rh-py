from flask import Flask, jsonify, make_response, request, abort
from pymongo import MongoClient
from bson.objectid import ObjectId 
import socket

app = Flask(__name__)

# In order to run the app locally
# client = MongoClient('localhost', 27017)

# In order to run the app on prod 
client = MongoClient('mongodb://mongo:27017/')

db = client['pizza_house']
collection = db['order']

@app.route("/")
def index():
    hostname = socket.gethostbyname()
    return jsonify(message=f"Welcome to the Pizza House! Running inside {hostname}!")

# 1. Welcome API
@app.route('/welcome', methods=['GET'])
def welcome():
    response = make_response(
        jsonify(
            {"0": "Welcome to Pizza House"}
        ), 
        200,
    )
    return response 


# 2. Accept Order API
@app.route('/order', methods=['POST'])
def order():
    request_data = request.get_json()
    id = collection.insert_one(request_data).inserted_id

    response = make_response(
        jsonify(
            {'id': str(id)}
        ), 
        201,
    )
    return response 

# 3 Get order details APIs
# 3.1. /getorders
@app.route('/getorders', methods=['GET'])
def getorders():
    documents = collection.find()
    response_list = [] 
    for document in documents:
        document['_id'] = str(document['_id'])
        response_list.append(document)
    
    response = make_response(
        jsonify(response_list), 
        200,
    )
    return response 


# 3.2 /getorders/id
@app.errorhandler(404)
def id_not_found(error):
    return '', 404

@app.route('/getorders/<order_id>', methods=['GET'])
def getordersid(order_id):
    
    documents = collection.find(
        {'_id': ObjectId(order_id)}
    )

    response_list = [] 
    for document in documents:
        document['_id'] = str(document['_id'])
        response_list.append(document)
    
    if len(response_list) == 0:
        abort(404)

    response = make_response(
        jsonify(response_list[0]), 
        200,
    )
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 
