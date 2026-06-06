# Import threading for running timers in separate threads
import threading

# Import datetime to create timestamps for alerts
from datetime import datetime

# Global dictionary to store all active monitors and their states
# Each monitor has an id as key and contains timeout, alert_email, status, and timer
monitors = {}


# Function triggered when a monitor timeout is reached without a heartbeat
# Changes the monitor status to "down" and logs an alert message
def trigger_alert(monitor_id):
    # Get the monitor object from the monitors dictionary
    monitor = monitors.get(monitor_id)
    # Check if monitor exists and is still in active status
    if monitor and monitor["status"] == "active":
        # Update status to "down" to indicate the device is not responding
        monitor["status"] = "down"
        # Print alert message with current UTC timestamp (in production, this would send an email)
        print(
            {
                "ALERT": f"Device {monitor_id} is down!",
                "time": datetime.utcnow().isoformat(),
            }
        )


# Function to start or restart a countdown timer for a specific monitor
# If a timer already exists, it's cancelled before starting a new one
def start_timer(monitor_id, timeout):
    # Get the monitor object from the monitors dictionary
    monitor = monitors[monitor_id]
    # Cancel any existing timer to prevent duplicate alerts
    if monitor.get("timer"):
        monitor["timer"].cancel()
    # Create a new threading.Timer that will call trigger_alert after timeout seconds
    # Pass monitor_id as an argument to trigger_alert function
    timer = threading.Timer(timeout, trigger_alert, args=[monitor_id])
    # Start the timer in a separate thread
    timer.start()
    # Store the timer object in the monitor dictionary for later reference/cancellation
    monitor["timer"] = timer
