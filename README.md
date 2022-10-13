# rh-py

## Screenshots

Flask Application and Consumer
![Application and Consumer](https://github.com/swarajpande4/rh-py/blob/main/images/app-consume.png?raw=true)

<br>

Order Queue on RabbitMQ
![Order Queue](https://github.com/swarajpande4/rh-py/blob/main/images/order_queue.png?raw=true)

<br>

Data getting inserted in MongoDB
![MongoDB](https://github.com/swarajpande4/rh-py/blob/main/images/mongodb.png?raw=true)

<br>

Fetching all orders 
![All Orders](https://github.com/swarajpande4/rh-py/blob/main/images/getorders.png?raw=true)

<br>

Fetching order by id
![Fetch Order by id](https://github.com/swarajpande4/rh-py/blob/main/images/getorder-id.png?raw=true)

<br>

Testing the application
![Testing](https://github.com/swarajpande4/rh-py/blob/main/images/unittest.png?raw=true)

<br>

## Running at localhost

Pre-requisites include Git, Python 3.4+ with **pip**, MongoDB, Erlang and RabbitMQ.
<br>
Links to the same can be found under the references section.
<br>
These are the steps to follow in order to run the project on local host: 
<br>

```
git clone https://github.com/swarajpande4/rh-py
```

```
cd rh-py
```

```
pip install virtualenv
python -m venv <name of environment>
source <name of environment>/bin/activate
pip install -r requirements.txt
```

<br>

The *flask application* is started via the following command and is accessible on *localhost:8080*
```
python app.py
```

The *consumer microservice* is started via the following command 
```
python consumer.py
```

<br>
The application (once started) can be tested via the following command 

```
python test_app.py
```

<br>

## Ports used in localhost 
- `localhost:8080` for Flask Application 
- `localhost:27017` for MongoDB 
- `localhost:15672` for RabbitMQ Management

<br>

## References 
- [Git](https://git-scm.com/)
- [Python3](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/2.2.x/)
- [MongoDB](https://www.mongodb.com/)
- [Erlang](https://www.erlang.org/)
- [RabbitMQ](https://www.rabbitmq.com/)