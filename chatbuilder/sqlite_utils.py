# chatbuilder/sqlite_utils.py
import sqlite3
from chatbuilder.models import ChatDataset, ChatSample, ChatMessage
from typing import List
import os

DB_FILE = "data/serialized/chat_dataset.db"

def initialize_db(db_path: str = DB_FILE):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            sample_id INTEGER,
            message_index INTEGER,
            role TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_sqlite(dataset: ChatDataset, db_path: str = DB_FILE):
    initialize_db(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM messages")
    for sample_id, sample in enumerate(dataset.samples):
        for idx, msg in enumerate(sample.messages):
            cursor.execute("""
                INSERT INTO messages (sample_id, message_index, role, content)
                VALUES (?, ?, ?, ?)
            """, (sample_id, idx, msg.role, msg.content))

    conn.commit()
    conn.close()

def load_from_sqlite(db_path: str = DB_FILE) -> ChatDataset:
    initialize_db(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT sample_id, message_index, role, content FROM messages ORDER BY sample_id, message_index")
    rows = cursor.fetchall()
    conn.close()

    samples_dict = {}
    for sample_id, msg_idx, role, content in rows:
        if sample_id not in samples_dict:
            samples_dict[sample_id] = []
        samples_dict[sample_id].append(ChatMessage(role=role, content=content))

    samples = [ChatSample(messages=messages) for _, messages in sorted(samples_dict.items())]
    return ChatDataset(samples=samples)
