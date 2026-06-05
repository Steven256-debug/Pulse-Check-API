# Pulse-Check-API (Watchdog Sentinel)

A Dead Man's Switch API built with FastAPI and Python.

## Architecture Diagram

Client → POST /monitors → Register Device + Start Timer
↓
Timer counts down
↓
Heartbeat received? → YES → Reset Timer
↓
NO
↓
ALERT: Device is down! 

## Setup Instructions

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run server: `uvicorn app:app --reload`

## API Documentation

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /monitors | Register a new monitor |
| GET | /monitors/{id} | Get monitor status |
| POST | /monitors/{id}/heartbeat | Reset countdown timer |
| POST | /monitors/{id}/pause | Pause monitoring |

## Developer's Choice Feature

Added `GET /monitors/{id}` endpoint to check the current status of any device monitor in real time. This makes the system more observable and useful for support engineers who need to quickly check if a device is active, paused or down without waiting for an alert.