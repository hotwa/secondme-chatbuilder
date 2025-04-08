from dataclasses import dataclass, field
from typing import List, Literal
import json
import pickle

@dataclass
class ChatMessage:
    role: Literal["system", "user", "assistant"]
    content: str

@dataclass
class ChatSample:
    messages: List[ChatMessage]

@dataclass
class ChatDataset:
    samples: List[ChatSample] = field(default_factory=list)

    def to_jsonl(self, filepath: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            for sample in self.samples:
                f.write(json.dumps({"messages": [m.__dict__ for m in sample.messages]}, ensure_ascii=False) + '\n')

    def to_pickle(self, filepath: str):
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def from_pickle(filepath: str) -> 'ChatDataset':
        with open(filepath, 'rb') as f:
            return pickle.load(f)
