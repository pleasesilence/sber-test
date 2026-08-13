from fastapi import FastAPI, Request
from threading import Lock
from dotenv import load_dotenv
import os
import time


class TTLStore:
    def __init__(self):
        self._data: dict[str, tuple[str, float]] = {}
        self._lock = Lock()

    def set(self, name: str, ip: str, ttl_seconds: int):
        with self._lock:
            self._data[name] = (ip, time.monotonic() + ttl_seconds)

    def get(self, name: str) -> str | None:
        with self._lock:
            entry = self._data.get(name)
            if entry is None:
                return None
            ip, expires_at = entry
            if time.monotonic() > expires_at:
                del self._data[name]
                return None
            return ip


load_dotenv()
ip_ttl = int(os.environ.get("IP_TTL", 60))

app = FastAPI()
store = TTLStore()

@app.get('/')
async def check_client_ip(request: Request, name: str | None = None):
    client_ip = request.client.host
    forwarded_info = request.headers.get("x-forwarded-for")
    client_ip = forwarded_info.split(',')[0].strip() if forwarded_info else client_ip

    if name:
        store.set(name, client_ip, ip_ttl)

    return {"client_ip": client_ip}

@app.get('/resolve/{name}')
async def resolve_name_for_ip(name: str):
    client_ip = store.get(name)
    if client_ip is not None:
        return {"status": "success", "name": name, "resolved_ip": client_ip}
    else:
        return {"status": "failure", "name": name}