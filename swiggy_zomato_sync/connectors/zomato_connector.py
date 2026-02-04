import requests
import json
import frappe

class ZomatoConnector:
    def __init__(self, client_id, client_secret, merchant_id):
        self.client_id = client_id
        self.client_secret = client_secret
        self.merchant_id = merchant_id
        self.base_url = "https://api.zomato.com/v2" # Mock/Placeholder URL

    def get_access_token(self):
        # Simulated OAuth Token Fetch
        return "mock_zomato_token"

    def fetch_orders(self):
        # Mock Data for testing
        mock_orders = [
            {
                "order_id": "ZM-2002",
                "customer": {"name": "Jane Smith", "phone": "9998887776"},
                "items": [
                    {"name": "Veg Burger", "qty": 2, "price": 120},
                    {"name": "Fries", "qty": 1, "price": 80}
                ],
                "charges": {"packing": 15, "delivery": 25},
                "total": 360,
                "status": "Completed"
            }
        ]
        return mock_orders
