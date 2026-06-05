from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from monitors import monitors, start_timer

app = FastAPI()


class MonitorInput(BaseModel):
    id: str
    timeout: int
    alert_email: str


@app.post("/monitors", status_code=201)
def register_monitor(data: MonitorInput):
    monitors[data.id] = {
        "timeout": data.timeout,
        "alert_email": data.alert_email,
        "status": "active",
        "timer": None,
    }
    start_timer(data.id, data.timeout)
    return {"message": f"Monitor {data.id} created successfully"}


@app.get("/monitors/{monitor_id}")
def get_monitor(monitor_id: str):
    if monitor_id not in monitors:
        raise HTTPException(status_code=404, detail="Monitor not found")
    monitor = monitors[monitor_id]
    return {
        "id": monitor_id,
        "status": monitor["status"],
        "timeout": monitor["timeout"],
        "alert_email": monitor["alert_email"],
    }


@app.post("/monitors/{monitor_id}/heartbeat")
def heartbeat(monitor_id: str):
    if monitor_id not in monitors:
        raise HTTPException(status_code=404, detail="Monitor not found")
    monitor = monitors[monitor_id]
    monitor["status"] = "active"
    start_timer(monitor_id, monitor["timeout"])
    return {"message": f"Heartbeat received for {monitor_id}"}


@app.post("/monitors/{monitor_id}/pause")
def pause_monitor(monitor_id: str):
    if monitor_id not in monitors:
        raise HTTPException(status_code=404, detail="Monitor not found")
    monitor = monitors[monitor_id]
    if monitor.get("timer"):
        monitor["timer"].cancel()
    monitor["status"] = "paused"
    return {"message": f"Monitor {monitor_id} paused"}
