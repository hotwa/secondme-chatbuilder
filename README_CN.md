# SecondMe ChatBuilder

一个用于构建 Chat Messages 格式数据的可视化工具，专为 [Second-Me MLX Training](https://github.com/mindverse/Second-Me) 项目设计。

## 功能

- 可视化构建 OpenAI-style messages 格式数据
- 支持导出为 `.jsonl`（训练数据）和 `.pkl`（序列化备份）
- 为 Apple Silicon 上的 MLX 微调流程准备数据

## 快速开始

```bash
pip install -r requirements.txt
python ui/gradio_app.py

### 🔧 功能特色

- 可视化编辑符合 OpenAI `messages` 格式的数据（角色 + 内容）
- 支持添加 / 删除 / 重排消息
- 可导出为：
  - `.jsonl` 格式（用于 MLX 训练）
  - `.pkl` 格式（用于本地编辑和保存）
- 与 Apple Silicon 上的 MLX 微调训练流程无缝对接

### 🚀 快速开始

```bash
pip install -r requirements.txt
python ui/gradio_app.py
```

### 📁 项目结构

```
secondme-chatbuilder/
├── chatbuilder/        # 核心数据结构与逻辑
├── ui/                 # Gradio 前端界面
├── data/               # 数据输入输出（原始 / 处理后 / 序列化）
├── scripts/            # 数据转化脚本（如 merged.json → jsonl）
├── requirements.txt
└── README.md
```

### 📦 导出格式示例
每条对话保存为如下格式：
```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "什么是量子计算？"},
    {"role": "assistant", "content": "量子计算是一种基于量子力学的计算方式..."}
  ]
}
```

### Sqlite 数据库 转化

```bash
# # 导出为 JSONL
python scripts/sqlite_to_file.py \
  --db data/serialized/chat_dataset.db \
  --format jsonl \
  --outdir data/processed


# # 导出为 Pickle
python scripts/sqlite_to_file.py \
  --db data/serialized/chat_dataset.db \
  --format pkl \
  --outdir data/serialized
```
