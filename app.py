# Import required libraries for building REST API and data validation
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from monitors import monitors, start_timer

# Create a FastAPI application instance
app = FastAPI()


# Define Pydantic model for validating monitor registration input
# This model ensures that POST requests contain id, timeout, and alert_email fields
class MonitorInput(BaseModel):
    id: str  # Unique identifier for the monitor
    timeout: int  # Timeout duration in seconds
    alert_email: str  # Email address to send alerts to


# POST endpoint to register a new monitor
# Takes monitor configuration data and creates an active monitor with a timer
@app.post("/monitors", status_code=201)
def register_monitor(data: MonitorInput):
    # Store monitor configuration in the monitors dictionary
    monitors[data.id] = {
        "timeout": data.timeout,  # How long before alert is triggered
        "alert_email": data.alert_email,  # Where to send alerts
        "status": "active",  # Current status of the monitor
        "timer": None,  # Thread timer object (will be set when started)
    }
    # Start the countdown timer for this monitor
    start_timer(data.id, data.timeout)
    # Return success message
    return {"message": f"Monitor {data.id} created successfully"}


# GET endpoint to retrieve monitor details by ID
# Returns the status, timeout, and alert email for a specific monitor
@app.get("/monitors/{monitor_id}")
def get_monitor(monitor_id: str):
    # Check if monitor exists, return 404 error if not found
    if monitor_id not in monitors:
        raise HTTPException(status_code=404, detail="Monitor not found")
    # Retrieve monitor data from the monitors dictionary
    monitor = monitors[monitor_id]
    # Return monitor information in a structured format
    return {
        "id": monitor_id,
        "status": monitor["status"],
        "timeout": monitor["timeout"],
        "alert_email": monitor["alert_email"],
    }


# POST endpoint to receive a heartbeat signal from a monitored device
# Resets the timer when a heartbeat is received, indicating the device is still alive
@app.post("/monitors/{monitor_id}/heartbeat")
def heartbeat(monitor_id: str):
    # Check if monitor exists, return 404 error if not found
    if monitor_id not in monitors:
        raise HTTPException(status_code=404, detail="Monitor not found")
    # Get the monitor object from the monitors dictionary
    monitor = monitors[monitor_id]
    # Update status to active when heartbeat is received
    monitor["status"] = "active"
    # Reset the timer - this prevents the alert from triggering
    start_timer(monitor_id, monitor["timeout"])
    # Return confirmation that heartbeat was received
    return {"message": f"Heartbeat received for {monitor_id}"}


# POST endpoint to pause a monitor
# Stops the countdown timer and sets the monitor to paused status
@app.post("/monitors/{monitor_id}/pause")
def pause_monitor(monitor_id: str):
    # Check if monitor exists, return 404 error if not found
    if monitor_id not in monitors:
        raise HTTPException(status_code=404, detail="Monitor not found")
    # Get the monitor object from the monitors dictionary
    monitor = monitors[monitor_id]
    # Cancel the existing timer to prevent alerts from triggering
    if monitor.get("timer"):
        monitor["timer"].cancel()
    # Set monitor status to paused
    monitor["status"] = "paused"
    # Return confirmation that monitor was paused
    return {"message": f"Monitor {monitor_id} paused"}
