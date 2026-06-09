#!/usr/bin/env python3
"""Randomly draw 爽点 (beats) for a given short-drama genre.

The model tends to reuse the same few beats. This gives *genuine* randomness so
each story feels different. Pools mirror references/genres.md (keep in sync).

Usage:
  python3 pick_beats.py --genre 草根逆袭
  python3 pick_beats.py --genre 复仇打脸 --n 10
  python3 pick_beats.py --list
"""
import argparse
import random
import sys

POOLS = {
    "草根逆袭": ["低谷开局", "被轻视", "天赋觉醒", "贵人相助", "破釜沉舟", "技能碾压",
                "身份反转", "绝地反击", "一战成名", "众人见证", "打脸羞辱", "知遇之恩",
                "回馈社会", "坚持不懈", "逆风翻盘", "扮猪吃虎", "实力打脸", "草根登顶"],
    "复仇打脸": ["含冤受辱", "隐忍蛰伏", "收集证据", "扮猪吃虎", "身份隐藏", "实力反转",
                "步步紧逼", "当众揭穿", "对手溃败", "墙倒众人推", "真相大白", "正义伸张",
                "化敌为友", "自我救赎", "强者归来"],
    "都市甜宠": ["命运相遇", "误会反差", "强势守护", "吃醋占有", "双向奔赴", "反差萌",
                "高调宠溺", "危难相救", "身份悬殊", "众人羡慕", "破除阻力", "当众官宣",
                "家人认可", "破镜重圆", "跨越鸿沟"],
    "霸总言情": ["命运相遇", "误会反差", "强势守护", "吃醋占有", "双向奔赴", "反差萌",
                "高调宠溺", "危难相救", "身份悬殊", "众人羡慕", "破除阻力", "当众官宣",
                "家人认可", "破镜重圆", "跨越鸿沟"],
    "悬疑反转": ["开场悬念", "信息差", "误导铺垫", "抽丝剥茧", "关键反转", "身份反转",
                "真凶意外", "伏笔回收", "细思极恐", "绝境破局", "智斗博弈", "真相大白",
                "多重反转", "闭环收尾"],
    "家庭伦理": ["误解积怨", "隐忍付出", "真相浮现", "亲情羁绊", "舍己为家", "知错和解",
                "守护承诺", "代际理解", "雪中送炭", "苦尽甘来", "团圆相聚", "宽容大度", "感恩回报"],
    "古装重生": ["重生归来", "先知优势", "改写命运", "宿敌再遇", "步步为营", "扮猪吃虎",
                "打脸前世仇人", "身份反转", "宫斗商战智胜", "护住所爱", "因果轮回",
                "强势翻盘", "众人惊叹"],
    "战神赘婿": ["隐藏身份", "被轻视", "绝境亮剑", "实力碾压", "一招制敌", "身份揭晓",
                "众人震惊", "强者相迎", "打脸豪门", "守护家人", "扮猪吃虎", "王者归来", "一言九鼎"],
    "搞笑沙雕": ["反差人设", "误会连环", "神转折", "自作自受", "装到翻车", "歪打正着",
                "群体捧哏", "打破第四面墙", "反差萌", "意外救场", "笑中带泪", "无厘头逆袭"],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--genre", default="")
    ap.add_argument("--n", type=int, default=0, help="draw count; default random 8-12")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    if args.list or not args.genre:
        print("可选题材：" + "、".join(POOLS.keys()))
        if not args.genre:
            return
    if args.genre not in POOLS:
        print(f"未知题材：{args.genre}（可叠加题材时自行混用）", file=sys.stderr)
        sys.exit(1)

    pool = POOLS[args.genre]
    n = args.n or random.randint(8, 12)
    n = min(n, len(pool))
    picks = random.sample(pool, n)
    print(f"【{args.genre}】随机抽取 {n} 个爽点：")
    for i, p in enumerate(picks, 1):
        print(f"  {i}. {p}")


if __name__ == "__main__":
    main()
