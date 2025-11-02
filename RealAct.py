import json
from json import JSONDecodeError
from pathlib import Path
import sys

# ========== 配置部分 ==========
# 你可以通过命令行传参数：python add_words.py 2025-10-29 "apple 苹果 banana 香蕉 red 红色"
# 或者直接在下面写死 date 和 words_str
# if len(sys.argv) >= 3:
#     date = sys.argv[1]
#     words_str = " ".join(sys.argv[2:])  # 剩余的合并为一个字符串
# else:
#     # 没传参数时使用默认（调试用）
#     date = "2025-10-29"
#     words_str = "apple 苹果 banana 香蕉 red 红色"

# ========== 主逻辑部分 ==========

file_path = Path("static/list.json")

# 尝试加载已有 JSON 数据
if file_path.exists():
    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (JSONDecodeError, ValueError):
        print("⚠️ list.json 文件损坏，将重新创建。")
        data = {}
else:
    data = {}

# 确保有日期
if date not in data:
    data[date] = {}

# 将字符串按空格分割（每两项为一组）
parts = words_str.strip().split()
if len(parts) % 2 != 0:
    print("❌ 输入错误：英文与中文必须成对！")
    sys.exit(1)

# 成对插入
for i in range(0, len(parts), 2):
    english = parts[i]
    chinese = parts[i + 1]
    data[date][english] = chinese

# 写回文件
with file_path.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ 已将 {len(parts)//2} 个单词插入到 {date} 中。")
