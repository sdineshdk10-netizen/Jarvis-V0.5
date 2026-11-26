"""Provider-neutral speech interface for JARVIS."""
from dataclasses import dataclass
from typing import Protocol

class SpeechProvider(Protocol):
    def synthesize(self, text: str, *, language: str, voice: str) -> bytes: ...

@dataclass
class VoiceEngine:
    provider: SpeechProvider
    voice: str
    def speak(self, reply: str, language: str = 'tanglish') -> bytes:
        if language not in ('ta', 'en', 'tanglish'):
            raise ValueError('Unsupported language')
        if not reply.strip():
            raise ValueError('Empty reply')
        return self.provider.synthesize(reply, language=language, voice=self.voice)
