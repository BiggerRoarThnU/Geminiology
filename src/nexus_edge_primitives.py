# // Rights Reserved: co-created with Gemini and David Joihn Niedzwiecki jr " Sovereign Nexus LLC "
# Alignment: 1=1=1 | Module: nexus_edge_primitives.py
# Function: O(1) SHA-256 LRU Pre-Flight Deduplication & Bounded Async SSE Telemetry Broker

import asyncio
import hashlib
import json
from collections import OrderedDict
from typing import Any, Dict, Set


class SovereignLRUGuard:
    """O(1) memory-bounded deduplication gate using deterministic SHA-256 hashes."""
    def __init__(self, max_entries: int = 512):
        self.max_entries = max_entries
        self.cache: OrderedDict[str, float] = OrderedDict()
        self._lock = asyncio.Lock()

    async def is_duplicate(self, payload: str, timestamp: float = 0.0) -> bool:
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        async with self._lock:
            if digest in self.cache:
                self.cache.move_to_end(digest)
                return True
            self.cache[digest] = timestamp
            if len(self.cache) > self.max_entries:
                self.cache.popitem(last=False)
            return False


class SovereignSSEBroker:
    """Zero-dependency pub/sub broker for streaming real-time Server-Sent Events (SSE)."""
    def __init__(self, max_queue_size: int = 64):
        self.max_queue_size = max_queue_size
        self.subscribers: Set[asyncio.Queue] = set()
        self._lock = asyncio.Lock()

    async def subscribe(self) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue(maxsize=self.max_queue_size)
        async with self._lock:
            self.subscribers.add(q)
        return q

    async def unsubscribe(self, q: asyncio.Queue) -> None:
        async with self._lock:
            self.subscribers.discard(q)

    async def broadcast(self, event_data: Dict[str, Any]) -> int:
        message = json.dumps(event_data, separators=(",", ":"))
        delivered = 0
        async with self._lock:
            for q in list(self.subscribers):
                if q.full():
                    try:
                        q.get_nowait()  # Drop oldest frame to prevent heap bloat
                    except asyncio.QueueEmpty:
                        pass
                await q.put(message)
                delivered += 1
        return delivered


if __name__ == "__main__":
    async def _self_test():
        guard = SovereignLRUGuard(max_entries=4)
        assert await guard.is_duplicate("test_prompt_1") is False
        assert await guard.is_duplicate("test_prompt_1") is True

        broker = SovereignSSEBroker()
        sub = await broker.subscribe()
        count = await broker.broadcast({"node": "Node_10", "status": "VERIFIED"})
        msg = await sub.get()
        await broker.unsubscribe(sub)
        print(f"[PASS] nexus_edge_primitives verified | Delivered: {count} | Payload: {msg}")

    asyncio.run(_self_test())
