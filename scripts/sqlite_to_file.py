# scripts/sqlite_to_file.py

import argparse
import os
from datetime import datetime

from chatbuilder.sqlite_utils import load_from_sqlite
from chatbuilder.io_utils import save_jsonl, save_pickle

def main():
    parser = argparse.ArgumentParser(description="Convert SQLite chat dataset to JSONL or Pickle.")
    parser.add_argument("--db", type=str, default="data/serialized/chat_dataset.db", help="Path to SQLite DB file.")
    parser.add_argument("--format", type=str, choices=["jsonl", "pkl"], required=True, help="Output format: jsonl or pkl.")
    parser.add_argument("--outdir", type=str, default="data/processed", help="Output directory.")
    args = parser.parse_args()

    dataset = load_from_sqlite(args.db)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    os.makedirs(args.outdir, exist_ok=True)

    if args.format == "jsonl":
        output_file = os.path.join(args.outdir, f"chat_dataset_{timestamp}.jsonl")
        save_jsonl(dataset, output_file)
    else:
        output_file = os.path.join(args.outdir.replace("processed", "serialized"), f"chat_dataset_{timestamp}.pkl")
        save_pickle(dataset, output_file)

    print(f"✅ Converted SQLite to {args.format.upper()}: {output_file}")

if __name__ == "__main__":
    main()





