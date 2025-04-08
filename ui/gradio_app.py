import re
from datetime import datetime
import gradio as gr
from chatbuilder.models import ChatMessage, ChatSample, ChatDataset
from chatbuilder.sqlite_utils import save_to_sqlite, load_from_sqlite

dataset = ChatDataset()
system_prompt = ""

def add_full_message(system_content, user_content, assistant_content):
    global system_prompt

    if not (system_content.strip() and user_content.strip() and assistant_content.strip()):
        return dataset.samples, "⚠️ 所有角色内容都不能为空", "", ""

    system_prompt = system_content  # 持续更新

    messages = [
        ChatMessage(role="system", content=system_content.strip()),
        ChatMessage(role="user", content=user_content.strip()),
        ChatMessage(role="assistant", content=assistant_content.strip())
    ]
    sample = ChatSample(messages=messages)
    dataset.samples.append(sample)

    return render_sample_table(), "✅ 对话已添加", "", ""

def export_dataset(fmt):
    now_str = datetime.now().strftime("%Y%m%d_%H%M")
    if fmt == "jsonl":
        filename = f"data/processed/chat_dataset_{now_str}.jsonl"
        dataset.to_jsonl(filename)
        return f"✅ 导出为 JSONL：{filename}"
    elif fmt == "pickle":
        filename = f"data/serialized/chat_dataset_{now_str}.pkl"
        dataset.to_pickle(filename)
        return f"✅ 导出为 Pickle：{filename}"
    return "❌ 未知导出格式"

# 新增 SQLite 导出函数
def export_to_sqlite():
    save_to_sqlite(dataset)
    return "✅ 数据已保存到 SQLite 数据库 chat_dataset.db"

# 新增 SQLite 导入函数
def import_from_sqlite():
    global dataset
    dataset = load_from_sqlite()
    return render_sample_table(), "✅ 已从 SQLite 成功导入"


def render_sample_table():
    table = []
    for idx, sample in enumerate(dataset.samples):
        sys_msg = next((m.content for m in sample.messages if m.role == "system"), "")
        usr_msg = next((m.content for m in sample.messages if m.role == "user"), "")
        asst_msg = next((m.content for m in sample.messages if m.role == "assistant"), "")
        table.append([idx, sys_msg, usr_msg, asst_msg])
    return table

def clear_all():
    dataset.samples.clear()
    return [], "✅ 所有对话已清空"

def export_dataset(fmt):
    if fmt == "jsonl":
        dataset.to_jsonl("data/processed/chat_dataset.jsonl")
        return "✅ 导出为 JSONL 成功"
    elif fmt == "pickle":
        dataset.to_pickle("data/serialized/chat_dataset.pkl")
        return "✅ 导出为 Pickle 成功"
    return "❌ 未知导出格式"

def delete_samples(index_input: str):
    if not index_input.strip():
        return render_sample_table(), "⚠️ 请输入要删除的 index，例如：1 或 1-3 或 1,3,5"

    total = len(dataset.samples)
    indices = set()

    for part in index_input.split(","):
        part = part.strip()
        if "-" in part:
            try:
                start, end = map(int, part.split("-"))
                indices.update(range(start, end + 1))
            except ValueError:
                return render_sample_table(), f"❌ 区间格式错误：{part}"
        else:
            try:
                indices.add(int(part))
            except ValueError:
                return render_sample_table(), f"❌ 数字格式错误：{part}"

    indices = sorted([i for i in indices if 0 <= i < total], reverse=True)
    for idx in indices:
        del dataset.samples[idx]

    return render_sample_table(), f"✅ 已删除 {len(indices)} 条样本"


with gr.Blocks() as demo:
    gr.Markdown("## 🧠 SecondMe ChatBuilder - 批量输入标准三段对话")

    with gr.Group():
        system_input = gr.Textbox(label="System Prompt", lines=2, placeholder="系统提示（只设一次，后续保留）")
        user_input = gr.Textbox(label="User Input", lines=2, placeholder="用户输入")
        assistant_input = gr.Textbox(label="Assistant Reply", lines=3, placeholder="助手回答")

        add_btn = gr.Button("✅ 添加一整条对话样本")
        add_status = gr.Textbox(label="状态", interactive=False)

    sample_table = gr.Dataframe(
        headers=["Index", "System", "User", "Assistant"],
        datatype=["number", "str", "str", "str"],
        label="📝 已添加对话样本",
        interactive=False
    )

    with gr.Row():
        delete_input = gr.Textbox(label="删除 Index（如：1,3 或 1-3）")
        delete_btn = gr.Button("🗑️ 删除指定样本")

    with gr.Row():
        clear_btn = gr.Button("♻️ 清空所有样本")
        export_jsonl = gr.Button("📦 导出 JSONL")
        export_pickle = gr.Button("💾 导出 Pickle")
        export_sqlite = gr.Button("🗃️ 导出 SQLite")  # 新增导出 SQLite 按钮
        import_sqlite = gr.Button("📂 从 SQLite 导入")  # 新增导入 SQLite 按钮

    export_status = gr.Textbox(label="导出/删除状态", interactive=False)

    # 绑定行为
    add_btn.click(
        add_full_message,
        inputs=[system_input, user_input, assistant_input],
        outputs=[sample_table, add_status, user_input, assistant_input]
    )

    delete_btn.click(delete_samples, inputs=delete_input, outputs=[sample_table, export_status])
    clear_btn.click(clear_all, outputs=[sample_table, export_status])
    export_jsonl.click(export_dataset, inputs=[gr.Textbox(value="jsonl", visible=False)], outputs=export_status)
    export_pickle.click(export_dataset, inputs=[gr.Textbox(value="pickle", visible=False)], outputs=export_status)
    export_sqlite.click(export_to_sqlite, outputs=export_status)
    import_sqlite.click(import_from_sqlite, outputs=[sample_table, export_status])

    demo.load(render_sample_table, outputs=sample_table)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
