import frappe
from frappe import _
from swiggy_zomato_sync.connectors.swiggy_connector import SwiggyConnector
from swiggy_zomato_sync.connectors.zomato_connector import ZomatoConnector
import json

@frappe.whitelist()
def sync_orders():
    settings = frappe.get_single("Swiggy Zomato Settings")
    
    if settings.enable_swiggy:
        swiggy = SwiggyConnector(settings.swiggy_client_id, settings.get_password("swiggy_client_secret"), settings.swiggy_merchant_id)
        orders = swiggy.fetch_orders()
        process_orders("Swiggy", orders, settings)
        
    if settings.enable_zomato:
        zomato = ZomatoConnector(settings.zomato_client_id, settings.get_password("zomato_client_secret"), settings.zomato_merchant_id)
        orders = zomato.fetch_orders()
        process_orders("Zomato", orders, settings)

def process_orders(platform, orders, settings):
    for order_data in orders:
        # Check if already synced
        if frappe.db.exists("Swiggy Zomato Order", {"external_order_id": order_data["order_id"]}):
            continue
            
        # Log the order
        log_doc = frappe.get_doc({
            "doctype": "Swiggy Zomato Order",
            "platform": platform,
            "external_order_id": order_data["order_id"],
            "order_status": order_data["status"],
            "customer_name": order_data["customer"]["name"],
            "customer_phone": order_data["customer"]["phone"],
            "order_total": order_data["total"],
            "raw_json": json.dumps(order_data, indent=2)
        })
        log_doc.insert(ignore_permissions=True)
        
        try:
            invoice_name = create_pos_invoice(order_data, settings)
            log_doc.pos_invoice = invoice_name
            log_doc.sync_status = "Synced"
            log_doc.save()
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), _("{0} Sync Failed").format(platform))
            log_doc.sync_status = "Failed"
            log_doc.save()

def create_pos_invoice(order_data, settings):
    # Mapping items to ERPNext Items
    items = []
    for item in order_data["items"]:
        # In a real scenario, we should have a mapping table
        # For now, we assume item_code = item name or we look it up
        item_code = frappe.db.get_value("Item", {"item_name": item["name"]}, "name") or item["name"]
        
        items.append({
            "item_code": item_code,
            "qty": item["qty"],
            "rate": item["price"],
            "warehouse": settings.default_warehouse
        })
        
    invoice = frappe.get_doc({
        "doctype": "Sales Invoice",
        "is_pos": 1,
        "pos_profile": settings.pos_profile,
        "company": settings.company,
        "customer": settings.default_customer,
        "posting_date": frappe.utils.today(),
        "items": items,
        "update_stock": 1,
        "payments": [
            {
                "mode_of_payment": "Cash", # Should be configurable
                "amount": order_data["total"],
                "account": frappe.db.get_value("POS Profile", settings.pos_profile, "account_for_cash_payment")
            }
        ]
    })
    
    # Add Taxes/Charges (Packing/Delivery)
    if order_data.get("charges"):
        for charge_type, amount in order_data["charges"].items():
            invoice.append("taxes", {
                "charge_type": "Actual",
                "account_head": "Sales - Service - T", # Placeholder
                "description": _("{0} Charges").format(charge_type.capitalize()),
                "tax_amount": amount
            })
            
    invoice.insert(ignore_permissions=True)
    invoice.submit()
    return invoice.name
