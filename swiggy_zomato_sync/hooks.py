app_name = "swiggy_zomato_sync"
app_title = "Swiggy Zomato Sync"
app_publisher = "Antigravity"
app_description = "Sync Swiggy and Zomato orders to ERPNext POS"
app_email = "admin@example.com"
app_license = "mit"

# Scheduled Tasks
# ---------------

scheduler_events = {
    "all": [
        "swiggy_zomato_sync.swiggy_zomato_sync.api.sync_orders"
    ],
    "daily": [
        # You could add daily cleanup jobs here
    ],
    "hourly": [
        # This will run based on settings if needed
    ],
}

# The actual frequency is managed inside the sync_orders function 
# by checking last_sync_time in settings, or simply letting Frappe 
# handle the "all" (every 4 mins) or hourly events.
