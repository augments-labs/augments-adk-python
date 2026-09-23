"""Voice pipeline — speak with an agent over speech-to-text and text-to-speech.

A ``VoicePipeline`` chains three stages: a ``STTModel``
transcribes audio, a ``VoiceWorkflow`` (typically
``SingleAgentVoiceWorkflow`` driving one agent) produces the text to
say, and a ``TTSModel`` synthesizes speech. The result is a
``StreamedAudioResult`` that yields
``VoiceStreamEvent`` objects — audio
chunks and turn/session lifecycle markers — as they are produced.

Audio is raw PCM ``bytes`` throughout; ``numpy`` is an optional helper
for converting captured sample arrays. The speech models are
provider-agnostic abstractions — concrete OpenAI implementations live in
``llms/openai/`` and are imported from there.

Example::

    from augments.adk import Agent
    from augments.adk.voice import (
        AudioInput,
        SingleAgentVoiceWorkflow,
        VoicePipeline,
    )
    from augments.adk.llms.openai import OpenAISTTModel, OpenAITTSModel

    pipeline = VoicePipeline(
        workflow=SingleAgentVoiceWorkflow(Agent(name="Assistant")),
        stt_model=OpenAISTTModel(),
        tts_model=OpenAITTSModel(),
    )
    result = await pipeline.run(AudioInput(data=pcm_bytes))
    async for event in result.stream():
        if event.type == "voice_stream_event_audio":
            play(event.data)

See ``docs/voice/`` and ``examples/voice/``.
"""

from __future__ import annotations

from augments.adk.voice.audio import (
    DEFAULT_CHANNELS,
    DEFAULT_SAMPLE_RATE,
    DEFAULT_SAMPLE_WIDTH,
    AudioInput,
    StreamedAudioInput,
    pcm16_from_float32,
    pcm16_from_int16,
)
from augments.adk.voice.events import (
    VoiceStreamEvent,
    VoiceStreamEventAudio,
    VoiceStreamEventError,
    VoiceStreamEventLifecycle,
)
from augments.adk.voice.exceptions import STTError, STTWebsocketError, TTSError, VoiceError
from augments.adk.voice.pipeline import VoicePipeline
from augments.adk.voice.pipeline_config import VoicePipelineConfig
from augments.adk.voice.result import StreamedAudioResult
from augments.adk.voice.splitter import TextSplitter, sentence_splitter
from augments.adk.voice.stt import (
    StreamedTranscriptionSession,
    STTModel,
    STTModelSettings,
    TurnDetection,
    TurnDetectionMode,
)
from augments.adk.voice.tts import TTSModel, TTSModelSettings
from augments.adk.voice.workflow import (
    SingleAgentVoiceWorkflow,
    VoiceWorkflow,
    VoiceWorkflowCallbacks,
)

__all__ = [
    "DEFAULT_CHANNELS",
    "DEFAULT_SAMPLE_RATE",
    "DEFAULT_SAMPLE_WIDTH",
    "AudioInput",
    "STTError",
    "STTModel",
    "STTModelSettings",
    "STTWebsocketError",
    "SingleAgentVoiceWorkflow",
    "StreamedAudioInput",
    "StreamedAudioResult",
    "StreamedTranscriptionSession",
    "TTSError",
    "TTSModel",
    "TTSModelSettings",
    "TextSplitter",
    "TurnDetection",
    "TurnDetectionMode",
    "VoiceError",
    "VoicePipeline",
    "VoicePipelineConfig",
    "VoiceStreamEvent",
    "VoiceStreamEventAudio",
    "VoiceStreamEventError",
    "VoiceStreamEventLifecycle",
    "VoiceWorkflow",
    "VoiceWorkflowCallbacks",
    "pcm16_from_float32",
    "pcm16_from_int16",
    "sentence_splitter",
]
