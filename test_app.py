import unittest 
from app import app, client 
from http import HTTPStatus

class TestAppClass(unittest.TestCase): 

    def setUp(self): 
        # Changing variables
        app.config['DEBUG'] = False 
        app.config['TESTING'] = True

        self.app = app.test_client()
        self.assertEqual(app.debug, False)

        # Deleting all old data in the pizza_house database
        self.db = client['pizza_house']
        self.db.order.drop() 

        self.db = client['pizza_house']
        self.collection = self.db['order']
        
        d = {'test0': ['p0', 'p1']}
        self.id = self.collection.insert_one(d).inserted_id

    def test_welcome_page(self):
        response = self.app.get('/welcome')
        self.assertEqual(response.status_code, HTTPStatus.OK)
    
    def test_get_all_orders(self):
        response = self.app.get('/getorders')
        self.assertEqual(response.status_code, HTTPStatus.OK)
    
    def test_get_one_order_OK(self):
        response = self.app.get(f'/getorders/{str(self.id)}')
        self.assertEqual(response.status_code, HTTPStatus.OK)
    
    def test_get_one_order_404(self):
        falseId = '0'*24
        response = self.app.get(f'/getorders/{falseId}')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
    
    def test_accept_order(self):
        d = {"test1": ["p0","p1"]}
        response = self.app.post('/order', json=d)
        self.assertEqual(response.status_code, HTTPStatus.ACCEPTED)
    
    def tearDown(self):
        self.db.order.drop() 

if __name__ == "__main__":
    unittest.main()