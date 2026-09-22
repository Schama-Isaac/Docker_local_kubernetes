import unittest

from app import app


class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        from app import routes
        routes.items.clear()
        self.client = app.test_client()
        self.client.testing = True

    def test_hello_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), 'Hello, Flask!')

    def test_health_route(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'status': 'ok'})

    def test_items_route_empty(self):
        response = self.client.get('/items')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'items': []})

    def test_add_item_route(self):
        response = self.client.post('/items', json={'name': 'item1'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {'message': 'Item added successfully'})

    def test_get_item_route(self):
        self.client.post('/items', json={'name': 'item1'})
        response = self.client.get('/items/0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'item': {'name': 'item1'}})

    def test_get_nonexistent_item_route(self):
        response = self.client.get('/items/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'error': 'Item not found'})


if __name__ == '__main__':
    unittest.main()
