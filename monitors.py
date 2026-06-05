import threading
import time
from datetime import datetime

monitors = {}


def trigger_alert(monitor_id):
    monitor = monitors.get(monitor_id)
    if monitor and monitor["status"] == "active":
        monitor["status"] = "down"
        print(
            {
                "ALERT": f"Device {monitor_id} is down!",
                "time": datetime.utcnow().isoformat(),
            }
        )


def start_timer(monitor_id, timeout):
    monitor = monitors[monitor_id]
    if monitor.get("timer"):
        monitor["timer"].cancel()
    timer = threading.Timer(timeout, trigger_alert, args=[monitor_id])
    timer.start()
    monitor["timer"] = timer
