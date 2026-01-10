# src/intelligence.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterator, List, Optional, Union, Tuple
import json
import threading
import queue
import urllib.request
import urllib.error

from settings import config


# ----------------------------
# Shared, always-updating state
# ----------------------------

@dataclass
class StreamState:
    """Holds the live-growing assistant response + useful metadata."""
    text: str = ""
    chunks: List[str] = field(default_factory=list)
    done: bool = False
    meta: Dict[str, Any] = field(default_factory=dict)

    def append(self, delta: str) -> None:
        if not delta:
            return
        self.chunks.append(delta)
        self.text += delta


@dataclass
class StreamEvent:
    """
    Event types you can build a UI around.
    - type="delta": new text arrived in `delta`
    - type="thinking": optional reasoning/thinking stream in `delta` (if model provides it)
    - type="tool_calls": tool call info (raw contains tool_calls array)
    - type="tool_result": result from executing a tool
    - type="done": stream finished; final metadata in state.meta
    """
    type: str
    delta: str = ""
    raw: Optional[dict] = None
    state: Optional[StreamState] = None
    tool_calls: Optional[List[dict]] = None


# ----------------------------
# Core (non-streaming) call
# ----------------------------

def chat(messages: List[dict], *, timeout_s: int = 300) -> str:
    """Simple non-streaming chat call to Ollama. Returns full assistant text."""
    base_url = config.get("ollama_base_url", "http://localhost:11434").rstrip("/")
    model = config.get("ollama_model", "mistral:7b-instruct-v0.3-q4_K_M")

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
    }

    req = urllib.request.Request(
        url=f"{base_url}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        raise RuntimeError(f"Couldn't reach Ollama at {base_url}. Is it running?") from e

    return (data.get("message") or {}).get("content", "")


# ----------------------------
# Streaming (single-threaded)
# ----------------------------

def stream_chat(
    messages: List[dict],
    *,
    tools: Optional[List[dict]] = None,
    state: Optional[StreamState] = None,
    on_event: Optional[Callable[[StreamEvent], None]] = None,
    timeout_s: int = 300,
) -> Iterator[StreamEvent]:
    """
    Stream /api/chat (NDJSON). Updates `state` as deltas arrive and yields StreamEvent.
    
    Args:
        messages: Chat messages
        tools: Optional list of tool definitions (JSON schema format)
        state: Optional StreamState to update
        on_event: Optional callback for events
        timeout_s: Request timeout
    """
    if state is None:
        state = StreamState()

    base_url = config.get("ollama_base_url", "http://localhost:11434").rstrip("/")
    model = config.get("ollama_model", "mistral:7b-instruct-v0.3-q4_K_M")

    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
    }
    
    # Add tools if provided
    if tools:
        payload["tools"] = tools

    req = urllib.request.Request(
        url=f"{base_url}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    def emit(ev: StreamEvent) -> StreamEvent:
        if on_event:
            on_event(ev)
        return ev

    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            for line in resp:
                if not line.strip():
                    continue

                obj = json.loads(line.decode("utf-8"))
                msg = obj.get("message") or {}

                # Text delta
                delta = msg.get("content") or ""
                if delta:
                    state.append(delta)
                    yield emit(StreamEvent(type="delta", delta=delta, raw=obj, state=state))

                # Optional fields (safe to ignore today, useful later)
                thinking = msg.get("thinking") or ""
                if thinking:
                    yield emit(StreamEvent(type="thinking", delta=thinking, raw=obj, state=state))

                # Tool calls from model
                tool_calls = msg.get("tool_calls")
                if tool_calls:
                    yield emit(StreamEvent(type="tool_calls", raw=obj, state=state, tool_calls=tool_calls))

                # Done chunk
                if obj.get("done"):
                    state.done = True
                    state.meta = obj
                    yield emit(StreamEvent(type="done", raw=obj, state=state))
                    return

    except urllib.error.URLError as e:
        raise RuntimeError(f"Couldn't reach Ollama at {base_url}. Is it running?") from e


# ----------------------------
# Streaming (background thread)
# ----------------------------

QueuedItem = Union[StreamEvent, Exception, None]  # event | error | sentinel


def stream_chat_threaded(
    messages: List[dict],
    *,
    tools: Optional[List[dict]] = None,
    state: Optional[StreamState] = None,
    on_event: Optional[Callable[[StreamEvent], None]] = None,
    timeout_s: int = 300,
) -> Tuple[StreamState, "queue.Queue[QueuedItem]", threading.Event, threading.Thread]:
    """
    Runs stream_chat in a background thread.

    Returns:
      (state, q, stop_event, thread)

    q receives:
      - StreamEvent instances
      - Exception (if something went wrong)
      - None sentinel (stream finished)
    """
    if state is None:
        state = StreamState()

    q: "queue.Queue[QueuedItem]" = queue.Queue()
    stop = threading.Event()

    def worker() -> None:
        try:
            for ev in stream_chat(messages, tools=tools, state=state, on_event=on_event, timeout_s=timeout_s):
                if stop.is_set():
                    break
                q.put(ev)
        except Exception as e:
            q.put(e)
        finally:
            q.put(None)

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    return state, q, stop, t
