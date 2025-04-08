import json
import pickle
from typing import List
from chatbuilder.models import ChatMessage, ChatSample, ChatDataset


def load_jsonl(filepath: str) -> ChatDataset:
    """Load a ChatDataset from a .jsonl file"""
    samples = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            messages = [ChatMessage(**msg) for msg in data["messages"]]
            samples.append(ChatSample(messages=messages))
    return ChatDataset(samples=samples)


def save_jsonl(dataset: ChatDataset, filepath: str):
    """Save a ChatDataset to a .jsonl file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        for sample in dataset.samples:
            f.write(json.dumps({"messages": [m.__dict__ for m in sample.messages]}, ensure_ascii=False) + '\n')


def save_pickle(dataset: ChatDataset, filepath: str):
    """Serialize a ChatDataset to a .pkl file"""
    with open(filepath, 'wb') as f:
        pickle.dump(dataset, f)


def load_pickle(filepath: str) -> ChatDataset:
    """Load a ChatDataset from a .pkl file"""
    with open(filepath, 'rb') as f:
        return pickle.load(f)

# from chatbuilder.io_utils import load_jsonl, save_pickle
# from chatbuilder.models import ChatDataset

# # 加载 jsonl 文件
# dataset = load_jsonl("data/processed/train.jsonl")

# # 保存为 pkl
# save_pickle(dataset, "data/serialized/train.pkl")
