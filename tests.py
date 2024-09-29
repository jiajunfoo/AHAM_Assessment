import unittest
from app import create_app, db, InvestmentFund, TestingConfig
import json

class InvestmentFundTestCase(unittest.TestCase):

    def setUp(self):
        # Use the TestingConfig here
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()  # Use test_client for making HTTP requests
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    # Test creating a new fund with valid data
    def test_create_fund(self):
        new_fund = {
            "name": "Tech Fund",
            "manager_name": "Alice",
            "description": "Investing in tech companies",
            "nav": 500000,
            "performance": 12.5
        }
        response = self.client.post('/funds', data=json.dumps(new_fund), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("Tech Fund", data['name'])

    # Test creating a fund with missing required fields
    def test_create_fund_missing_fields(self):
        incomplete_fund = {
            "description": "Investing in renewable energy",
            "nav": 400000,
            "performance": 10.0
        }
        response = self.client.post('/funds', data=json.dumps(incomplete_fund), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Missing required fields", data['error'])

    # Test creating a fund with invalid data types
    def test_create_fund_invalid_data_type(self):
        invalid_fund = {
            "name": "Energy Fund",
            "manager_name": "Tom",
            "description": "Investing in renewable energy",
            "nav": "invalid_nav",
            "performance": "invalid_performance"
        }
        response = self.client.post('/funds', data=json.dumps(invalid_fund), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("NAV and performance must be numbers", data['error'])

    # Test retrieving a specific fund
    def test_get_fund(self):
        new_fund = InvestmentFund(
            name="Health Fund", manager_name="Bob", description="Investing in healthcare", nav=300000, performance=8.9
        )
        with self.app.app_context():
            db.session.add(new_fund)
            db.session.commit()
            fund_id = new_fund.fund_id

        response = self.client.get(f'/funds/{fund_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("Health Fund", data['name'])

    # Test updating a fund's performance
    def test_update_fund_performance(self):
        new_fund = InvestmentFund(
            name="Tech Fund", manager_name="Alice", description="Investing in tech", nav=500000, performance=12.5
        )
        with self.app.app_context():
            db.session.add(new_fund)
            db.session.commit()
            fund_id = new_fund.fund_id

        update_data = {"performance": 15.0}
        response = self.client.put(f'/funds/{fund_id}', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['performance'], 15.0)

    # Test updating a fund with invalid performance data
    def test_update_fund_invalid_performance(self):
        new_fund = InvestmentFund(
            name="Tech Fund", manager_name="Alice", description="Investing in tech", nav=500000, performance=12.5
        )
        with self.app.app_context():
            db.session.add(new_fund)
            db.session.commit()
            fund_id = new_fund.fund_id

        invalid_update = {"performance": "invalid"}
        response = self.client.put(f'/funds/{fund_id}', data=json.dumps(invalid_update), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Invalid 'performance' value", data['message'])

    # Test deleting a fund
    def test_delete_fund(self):
        new_fund = InvestmentFund(
            name="Tech Fund", manager_name="Alice", description="Investing in tech", nav=500000, performance=12.5
        )
        with self.app.app_context():
            db.session.add(new_fund)
            db.session.commit()
            fund_id = new_fund.fund_id

        response = self.client.delete(f'/funds/{fund_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Fund deleted successfully", json.loads(response.data)['message'])

    # Test retrieving a non-existent fund
    def test_get_non_existent_fund(self):
        response = self.client.get('/funds/9999')  # Assuming fund_id 9999 doesn't exist
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn("Resource not found", data['error'])

    # Test deleting a non-existent fund
    def test_delete_non_existent_fund(self):
        response = self.client.delete('/funds/9999')  # Assuming fund_id 9999 doesn't exist
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn("Resource not found", data['error'])
        
    # Test updating fund performance and nav
    def test_update_fund_only_performance(self):
        original_fund = InvestmentFund(
            name="Tech Fund", manager_name="Alice", description="Tech investments", nav=500000, performance=12.5
        )
        with self.app.app_context():
            db.session.add(original_fund)
            db.session.commit()
            fund_id = original_fund.fund_id

        update_data = {"performance": 5, "nav": 1000}

        response = self.client.put(f'/funds/{fund_id}', data=json.dumps(update_data), content_type='application/json')

        # Step 3: Verify the status code
        self.assertEqual(response.status_code, 200)  # 200 OK

        # Step 4: Verify that only 'performance' was updated and other fields remain unchanged
        data = json.loads(response.data)
        self.assertEqual(data['performance'], 5.0)  # Performance should be updated
        self.assertEqual(data['nav'], 500000)  # nav should remain unchanged
        self.assertEqual(data['description'], "Tech investments")  # description should remain unchanged
        self.assertEqual(data['manager_name'], "Alice")  # manager_name should remain unchanged


if __name__ == '__main__':
    unittest.main()
