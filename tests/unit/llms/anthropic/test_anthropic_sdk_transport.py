"""AnthropicLLM against the real ``anthropic`` client over a mock transport.

The other suites replace ``messages.create`` with a mock, so they cannot see
what the SDK itself accepts. These tests keep the SDK in the loop and stop at
the HTTP transport: each request is recorded and answered with a canned
response, which checks both that the SDK accepts the call and what reaches
the wire.
"""

from __future__ import annotations

import json
from typing import Any

import httpx
import httpx2
from anthropic import AsyncAnthropic

from augments.adk.llms.anthropic import AnthropicLLM
from augments.adk.llms.llm_config import LLMConfig

_MESSAGE = {
    "id": "msg_1",
    "type": "message",
    "role": "assistant",
    "model": "claude-sonnet-4-5",
    "content": [{"type": "text", "text": "Hi!"}],
    "stop_reason": "end_turn",
    "stop_sequence": None,
    "usage": {"input_tokens": 10, "output_tokens": 5},
}

_STREAM_EVENTS: list[tuple[str, dict[str, Any]]] = [
    ("message_start", {"type": "message_start", "message": {**_MESSAGE, "content": [], "stop_reason": None}}),
    (
        "content_block_start",
        {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}},
    ),
    (
        "content_block_delta",
        {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "Hi!"}},
    ),
    ("content_block_stop", {"type": "content_block_stop", "index": 0}),
    (
        "message_delta",
        {
            "type": "message_delta",
            "delta": {"stop_reason": "end_turn", "stop_sequence": None},
            "usage": {"output_tokens": 5},
        },
    ),
    ("message_stop", {"type": "message_stop"}),
]


class _Recorder:
    """Answers every request with a canned response and keeps the requests."""

    def __init__(self, *, stream: bool) -> None:
        self.requests: list[httpx2.Request] = []
        self._stream = stream

    def __call__(self, request: httpx2.Request) -> httpx2.Response:
        self.requests.append(request)
        if self._stream:
            body = "".join(f"event: {name}\ndata: {json.dumps(data)}\n\n" for name, data in _STREAM_EVENTS)
            return httpx2.Response(200, headers={"content-type": "text/event-stream"}, content=body.encode())
        return httpx2.Response(200, json=_MESSAGE)

    def body(self) -> dict[str, Any]:
        assert len(self.requests) == 1
        return json.loads(self.requests[0].content)


def _llm_over(recorder: _Recorder) -> AnthropicLLM:
    llm = AnthropicLLM(model="claude-sonnet-4-5", api_key="test")
    llm._client = AsyncAnthropic(
        api_key="test",
        max_retries=0,
        http_client=httpx2.AsyncClient(transport=httpx2.MockTransport(recorder)),
    )
    return llm


async def test_plain_call_sends_no_sampling_fields() -> None:
    recorder = _Recorder(stream=False)

    response = await _llm_over(recorder).acomplete(messages="hello")

    assert response.content == "Hi!"
    body = recorder.body()
    assert "temperature" not in body
    assert "top_p" not in body
    assert "top_k" not in body


async def test_sampling_settings_reach_the_request_body() -> None:
    recorder = _Recorder(stream=False)

    await _llm_over(recorder).acomplete(
        messages="hello",
        llm_config=LLMConfig(temperature=0.2, top_p=0.9, top_k=40),
    )

    body = recorder.body()
    assert body["temperature"] == 0.2
    assert body["top_p"] == 0.9
    assert body["top_k"] == 40


async def test_extra_body_overrides_a_sampling_setting() -> None:
    recorder = _Recorder(stream=False)

    await _llm_over(recorder).acomplete(
        messages="hello",
        llm_config=LLMConfig(temperature=0.2, extra_body={"temperature": 0.5}),
    )

    assert recorder.body()["temperature"] == 0.5


async def test_httpx_timeout_reaches_the_transport() -> None:
    recorder = _Recorder(stream=False)

    await _llm_over(recorder).acomplete(
        messages="hello",
        llm_config=LLMConfig(timeout=httpx.Timeout(12.0, connect=3.0)),
    )

    timeout = recorder.requests[0].extensions["timeout"]
    assert timeout == {"connect": 3.0, "read": 12.0, "write": 12.0, "pool": 12.0}


async def test_float_timeout_reaches_the_transport() -> None:
    recorder = _Recorder(stream=False)

    await _llm_over(recorder).acomplete(messages="hello", llm_config=LLMConfig(timeout=7.5))

    timeout = recorder.requests[0].extensions["timeout"]
    assert timeout == {"connect": 7.5, "read": 7.5, "write": 7.5, "pool": 7.5}


async def test_streaming_call_sends_sampling_settings_and_yields_text() -> None:
    recorder = _Recorder(stream=True)

    stream = await _llm_over(recorder).acomplete(
        messages="hello",
        llm_config=LLMConfig(temperature=0.2),
        stream=True,
    )
    events = [event async for event in stream]

    body = recorder.body()
    assert body["stream"] is True
    assert body["temperature"] == 0.2
    done = [event for event in events if event.type == "done"]
    assert len(done) == 1
    assert done[0].response is not None
    assert done[0].response.content == "Hi!"
