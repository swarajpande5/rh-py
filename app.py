from flask import Flask, jsonify, make_response, request, abort
from http import HTTPStatus
from pymongo import MongoClient
from bson.objectid import ObjectId 
import json
import pika

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client['pizza_house']
collection = db['order']


# 1. Welcome API
@app.route('/welcome', methods=['GET'])
def welcome():
    try:
        response = make_response(
            jsonify(
                {"0": "Welcome to Pizza House"}
            ), 
            HTTPStatus.OK,
        )
        return response
    except:
        response = make_response(
            jsonify(
                {"0:": "Error occurred!"}
            ),
            HTTPStatus.BAD_REQUEST
        )
        return response



# 2. Accept Order API
# @app.route('/order', methods=['POST'])
# def order():
#     try:
#         request_data = request.get_json()
#         id = collection.insert_one(request_data).inserted_id

#         response = make_response(
#             jsonify(
#                 {'id': str(id)}
#             ), 
#             HTTPStatus.CREATED,
#         )
#         return response 
#     except:
#         response = make_response(
#             jsonify(
#                 {"0:": "Error occurred!"}
#             ),
#             HTTPStatus.BAD_REQUEST
#         )
#         return response


# 3 Get order details APIs
# 3.1. /getorders
@app.route('/getorders', methods=['GET'])
def getorders():
    try:
        documents = collection.find()
        response_list = [] 
        for document in documents:
            document['_id'] = str(document['_id'])
            response_list.append(document)
        
        response = make_response(
            jsonify(response_list), 
            HTTPStatus.OK,
        )
        return response 
    except:
        response = make_response(
            jsonify(
                {"0:": "Error occurred!"}
            ),
            HTTPStatus.BAD_REQUEST
        )
        return response


# 3.2 /getorders/id
@app.errorhandler(404)
def id_not_found(error):
    return '', HTTPStatus.NOT_FOUND

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


# 4. Introducing the Message Queue
# NOTE: In order to process the requests in the queue, consume.py should be used
@app.route('/order', methods=['POST'])
def order():
    credentials = pika.PlainCredentials('admin', 'admin')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel() 
    channel.queue_declare(queue='order_queue')

    persist = pika.BasicProperties(delivery_mode=2) # Making message persistent

    request_data = request.get_json()
    request_data_string = json.dumps(request_data)
    channel.basic_publish(exchange='', routing_key='order_queue', body=request_data_string, properties=persist)

    connection.close()

    response = make_response(
        jsonify(
            {'0': "Order placed in queue"}
        ), 
        HTTPStatus.ACCEPTED,
    )
    return response 


if __name__ == '__main__':
    app.run(port=8080, debug=True) 
