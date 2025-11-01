import re

input_file = "aaa.txt"
output_file = "cleaned_words.txt"

with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

result = []
for line in lines:
    # 1. 删除开头的数字和点
    line = re.sub(r"^\d+\.", "", line.strip())

    # 2. 提取英文单词
    match = re.match(r"([A-Za-z\-']+)\s+", line)
    if not match:
        continue
    word = match.group(1)

    # 3. 删除音标和考频部分（即中括号和圆括号）
    cleaned = re.sub(r"\[.*?\]|\（.*?\）|\(.*?\)", "", line)

    # 4. 去掉单词部分，只保留释义
    meaning = cleaned.replace(word, "", 1).strip()

    # 5. 删除释义中多余空格（比如“n. 缺点；瑕疵” -> “n.缺点；瑕疵”）
    meaning = re.sub(r"\s+", "", meaning)

    # 6. 合并输出：单词 + 空格 + 释义
    result.append(f"{word} {meaning}")

# 写入输出文件
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(result))

print("✅ 转换完成，结果已保存到", output_file)
