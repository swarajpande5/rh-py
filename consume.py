# This file will run in a different microservice and
# will act as the consumer process of the message in the queue.

import pika 
import json
import sys 
import os
import time
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['pizza_house']
collection = db['order']

def main():
    credentials = pika.PlainCredentials('admin', 'admin')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel() 
    channel.queue_declare(queue='order_queue')

    def callback(ch, method, properties, body):
        time.sleep(5)                                  # Any time consuming process ~ 10 seconds
        request_data = json.loads(body)
        id = collection.insert_one(request_data).inserted_id 
        print(f" [x] Inserted {str(id)}")
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Once the task is completed, send its acknowledgment
        return id                                       # id response returned when acknowledgment has been sent

    channel.basic_consume(queue='order_queue', on_message_callback=callback)

    print(' [*] Waiting for order requests. To exit press CTRL + C')
    channel.start_consuming() 


if __name__ == '__main__':
    try:
        main() 
    except KeyboardInterrupt:
        print('Interrupted')
        try: 
            sys.exit(0)
        except SystemExit:
            os._exit(0)