import json
from json import JSONDecodeError
from pathlib import Path

# ========= 文件路径 =========
TXT_FILE = Path("word.txt")
JSON_FILE = Path("list.json")

# ========= 读取已有 JSON（如有） =========
if JSON_FILE.exists():
    try:
        with JSON_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (JSONDecodeError, ValueError):
        print("⚠️ list.json 文件损坏，将重新创建。")
        data = {}
else:
    data = {}

# ========= 读取 word.txt =========
if not TXT_FILE.exists():
    print("❌ 找不到 word.txt 文件！")
    exit(1)

with TXT_FILE.open("r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

current_date = None

for line in lines:
    # 判断是否是日期行（格式类似 10/14 或 2025-10-29）
    if "/" in line or "-" in line:
        current_date = line
        if current_date not in data:
            data[current_date] = {}
    else:
        if not current_date:
            print(f"❌ 错误：在 '{line}' 前未定义日期！")
            continue

        parts = line.split()
        if len(parts) % 2 != 0:
            print(f"⚠️ 警告：{current_date} 下这一行英文和中文不成对：{line}")
            continue

        # 每两个为一组
        for i in range(0, len(parts), 2):
            eng = parts[i]
            chi = parts[i + 1]
            data[current_date][eng] = chi

# ========= 写回 JSON =========
with JSON_FILE.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ 所有数据已写入 list.json")
