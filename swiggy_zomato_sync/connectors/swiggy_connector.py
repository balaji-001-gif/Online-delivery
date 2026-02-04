import requests
import json
import frappe

class SwiggyConnector:
    def __init__(self, client_id, client_secret, merchant_id):
        self.client_id = client_id
        self.client_secret = client_secret
        self.merchant_id = merchant_id
        self.base_url = "https://partner.swiggy.com/api/v1" # Mock/Placeholder URL

    def get_access_token(self):
        # Simulated OAuth Token Fetch
        # In real scenario, this would call Swiggy's Auth API
        return "mock_swiggy_token"

    def fetch_orders(self):
        # Simulated Order Fetch
        # Real implementation would call GET /orders with Auth headers
        
        # Mock Data for testing
        mock_orders = [
            {
                "order_id": "SW-1001",
                "customer": {"name": "John Doe", "phone": "9876543210"},
                "items": [
                    {"name": "Margherita Pizza", "qty": 1, "price": 250},
                    {"name": "Coke", "qty": 2, "price": 50}
                ],
                "charges": {"packing": 20, "delivery": 30},
                "total": 400,
                "status": "Delivered"
            }
        ]
        return mock_orders
