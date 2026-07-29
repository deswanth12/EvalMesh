import asyncio
from typing import Dict, List, Callable, Any

class AsyncEventBus:
    """
    Lightweight Event Bus for Decoupled Telemetry, Audit Logs, and Analytics.
    Allows non-blocking event publishing after LLM response delivery.
    """
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}

    def subscribe(self, event_type: str, handler: Callable[[Dict[str, Any]], None]):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def publish(self, event_type: str, data: Dict[str, Any]):
        handlers = self._subscribers.get(event_type, [])
        for handler in handlers:
            try:
                handler(data)
            except Exception:
                pass

event_bus = AsyncEventBus()
