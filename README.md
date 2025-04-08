# 📚 SecondMe ChatBuilder

SecondMe ChatBuilder is a lightweight visual editor for building and managing structured conversation data (`messages` format) for fine-tuning LLMs on Apple Silicon using the MLX training framework. It is designed to support the [Second-Me](https://github.com/mindverse/Second-Me) project, providing a user-friendly interface for preparing training data in OpenAI-style format.

### 🔧 Features

- Visual chat editor for messages (`role`: system, user, assistant)
- Add, delete, and reorder message turns
- Save conversation samples as:
  - `.jsonl` — for MLX training
  - `.pkl` — for local backup or editing
  - SQLite database — for persistent storage
- Seamless integration with MLX training pipelines

### 🚀 Quick Start

```bash
pip install -r requirements.txt
python ui/gradio_app.py
```

### 📁 Project Structure

```
secondme-chatbuilder/
├── chatbuilder/        # Core data classes & logic
├── ui/                 # Gradio-based visual interface
├── data/               # Raw / processed / serialized outputs
├── scripts/            # Conversion scripts for MLX
├── requirements.txt
└── README.md
```

### 📦 Output Format
Each saved conversation will be exported like this:
```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is quantum computing?"},
    {"role": "assistant", "content": "Quantum computing is..."}
  ]
}
```

### SQLite Database Operations

```bash
# Export to JSONL
python scripts/sqlite_to_file.py \
  --db data/serialized/chat_dataset.db \
  --format jsonl \
  --outdir data/processed

# Export to Pickle
python scripts/sqlite_to_file.py \
  --db data/serialized/chat_dataset.db \
  --format pkl \
  --outdir data/serialized
```
