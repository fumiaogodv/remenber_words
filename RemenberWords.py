import json
import random

# ====== 加载词汇 JSON 文件 ======
with open("static/list.json", "r", encoding="utf-8") as f:
    data = json.load(f)


def show_all_dates():
    """显示所有日期"""
    print("\n📅 所有日期如下：")
    for i, date in enumerate(data.keys(), 1):
        print(f"{i}. {date}")
    print()


def show_words_by_date(date):
    """显示指定日期的所有英文单词"""
    if date not in data:
        print("❌ 找不到该日期，请重新输入。")
        return

    words = list(data[date].keys())
    print(f"\n📘 {date} 的单词列表：")
    for w in words:
        print(w)

    while True:
        choice = input("\n输入 1 返回上一级，或输入 3 查看中英文对照：").strip()
        if choice == "1":
            break
        elif choice == "3":
            print("\n📖 英文 - 中文 对照表：")
            for w, meaning in data[date].items():
                print(f"{w}  →  {meaning}")
            print()
        else:
            print("⚠️ 无效输入，请重新选择。")


def random_words_test(n=20):
    """随机抽取 n 个单词（先显示英文，再按键显示中英文）"""
    all_words = []
    for date, words in data.items():
        for en, zh in words.items():
            all_words.append((en, zh))

    sample = random.sample(all_words, min(n, len(all_words)))

    print(f"\n🎲 随机抽取 {len(sample)} 个英文单词如下：\n")
    for en, _ in sample:
        print(en)
    print("\n（输入任意数字显示答案，输入 q 返回主菜单）")

    while True:
        ans = input("👉 请输入：").strip()
        if ans.lower() == "q":
            break
        elif ans.isdigit() or ans == "":
            print("\n📖 英文 - 中文 对照：")
            for en, zh in sample:
                print(f"{en}  →  {zh}")
            print("\n✅ 复习完毕，输入 q 返回主菜单。")
        else:
            print("⚠️ 无效输入，请输入数字或 q。")


# ====== 主循环 ======
def main():
    print("=== 欢迎使用单词记忆程序 ===")
    print("功能：")
    print("1. 浏览所有日期并查看单词")
    print("2. 随机抽取 20 个单词复习")
    print("q. 退出程序\n")

    while True:
        cmd = input("请输入指令（1：浏览所有日期并查看单词/2：随机抽取 20 个单词复习/q）：").strip()

        if cmd == "1":
            show_all_dates()
            sub = input("输入 1 返回上一级 或 2 进入某个日期查看单词：").strip()
            if sub == "1":
                continue
            elif sub == "2":
                date = input("请输入日期（例如 10/15）：").strip()
                show_words_by_date(date)
            else:
                print("⚠️ 无效输入。")

        elif cmd == "2":
            random_words_test()

        elif cmd.lower() == "q":
            print("👋 再见，欢迎下次使用！")
            break

        else:
            print("⚠️ 无效指令，请重新输入。")


if __name__ == "__main__":
    main()
