#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麦太医 · 诊断证明书生成器（命令行版）
=====================================

用法：
    python3 report_card.py --type spicy
    python3 report_card.py --type bigmac --meal "巨无霸超值套餐" --cal 940 --protein 38

产出：
    一份可分享的自包含 HTML 诊断证明书（含主诉、诊断、六维口味基因、Rp. 处方笺、医嘱、门诊印章）。

说明：
    网页版（index.html）为完整问诊流程；本脚本用于「已知体质、快速出诊断书」的场景，
    六维得分为该体质的典型画像，接入 MCP 时可覆盖套餐与营养数据。
"""
import argparse
import html
import json
import os
import sys
from datetime import datetime

DIM_ORDER = ["辣度", "甜度", "冰爽", "饱腹", "分享", "治愈"]

TYPES = {
    "spicy": {
        "name": "麦辣热血型", "emoji": "🌶️", "tagline": "无辣不欢的行动派",
        "color": "#E82A1E", "color2": "#B3140F",
        "dx": "辣度依赖（中度）",
        "chief": "近期频繁渴望辛辣刺激，尤其在疲惫或情绪低落时，对「第一口就上头」的辣感有明显依赖。",
        "dims": {"辣度": 98, "甜度": 35, "冰爽": 70, "饱腹": 55, "分享": 50, "治愈": 50},
        "rx": [("麦辣鸡腿堡", "1 个"), ("中薯条", "1 份"), ("中可乐", "1 杯")],
        "meal": "麦辣鸡腿堡超值套餐", "cal": 790, "pro": 32,
        "advice": "辣爽可以，但别让胃替你买单。配冰饮时记得少冰，空腹别硬扛。",
    },
    "bigmac": {
        "name": "巨无霸稳健型", "emoji": "🍔", "tagline": "靠谱本谱，抗饿担当",
        "color": "#DA291C", "color2": "#B01F14",
        "dx": "饱腹感焦虑（轻度）",
        "chief": "主食缺位时易出现明显不安，进食以「顶饱、有层次、不出错」为首要诉求。",
        "dims": {"辣度": 50, "甜度": 40, "冰爽": 62, "饱腹": 96, "分享": 62, "治愈": 65},
        "rx": [("巨无霸", "1 个"), ("中薯条", "1 份"), ("中可乐", "1 杯")],
        "meal": "巨无霸超值套餐", "cal": 940, "pro": 38,
        "advice": "稳健是优点，偶尔也允许自己「不那么均衡」，尝一口甜筒奖励努力生活的自己。",
    },
    "nuggets": {
        "name": "麦乐鸡治愈型", "emoji": "🍗", "tagline": "温柔的小确幸收藏家",
        "color": "#F5A623", "color2": "#D98A10",
        "dx": "情绪性进食（轻度）",
        "chief": "情绪波动期倾向选择熟悉、小份、可慢慢吃的食物，以此获得安全感。",
        "dims": {"辣度": 35, "甜度": 65, "冰爽": 60, "饱腹": 60, "分享": 50, "治愈": 97},
        "rx": [("麦乐鸡（6 块）", "1 盒"), ("中薯条", "1 份"), ("甜酸酱", "2 包")],
        "meal": "麦乐鸡（6块）+ 薯条", "cal": 720, "pro": 28,
        "advice": "治愈自己很重要，但要警惕情绪化进食。规律三餐，才是温柔的长期主义。",
    },
    "cola": {
        "name": "冰可乐清爽型", "emoji": "🥤", "tagline": "理性轻盈的效率控",
        "color": "#2B8CC4", "color2": "#1B6E9E",
        "dx": "冰饮依赖（中度）",
        "chief": "对饮品的冰感与清爽度要求较高，偏好低负担、可快速解决的一餐。",
        "dims": {"辣度": 40, "甜度": 30, "冰爽": 98, "饱腹": 70, "分享": 55, "治愈": 55},
        "rx": [("双层吉士汉堡", "1 个"), ("零度可乐", "1 杯"), ("玉米杯", "1 份")],
        "meal": "双层吉士 + 零度可乐 + 玉米杯", "cal": 520, "pro": 24,
        "advice": "清爽型自带控卡天赋，但蛋白质别落下。轻盈不等于「饿着自己」。",
    },
    "cone": {
        "name": "甜筒小确幸型", "emoji": "🍦", "tagline": "及时行乐的甜党",
        "color": "#E94E77", "color2": "#C4315A",
        "dx": "糖分渴望（轻度）",
        "chief": "对甜味有持续偏好，常在餐后或情绪低落时需要一份甜品完成「心理收尾」。",
        "dims": {"辣度": 45, "甜度": 99, "冰爽": 55, "饱腹": 50, "分享": 65, "治愈": 75},
        "rx": [("圆筒冰淇淋", "1 支"), ("香芋派", "1 个"), ("小薯条", "1 份")],
        "meal": "圆筒 + 香芋派 + 小薯", "cal": 460, "pro": 6,
        "advice": "甜是奖赏，不是日常。用一支甜筒换走烦恼可以，别换来超标。",
    },
    "fries": {
        "name": "薯条元气型", "emoji": "🍟", "tagline": "社交电池永远满格",
        "color": "#F0A81E", "color2": "#C9820E",
        "dx": "社交型进食（活跃）",
        "chief": "进食愉悦感高度依赖「刚出锅、热乎、能分享」的场景，独食时满足感明显下降。",
        "dims": {"辣度": 60, "甜度": 45, "冰爽": 50, "饱腹": 60, "分享": 95, "治愈": 70},
        "rx": [("大薯条", "1 份"), ("麦辣鸡腿堡", "1 个"), ("中可乐", "1 杯")],
        "meal": "大薯 + 麦辣鸡腿堡 + 可乐", "cal": 890, "pro": 30,
        "advice": "元气满满，但记得给蔬菜和蛋白质留点位置，别让薯条独挑大梁。",
    },
}


def build_report_card(key, meal=None, cal=None, protein=None, out_dir=None):
    T = TYPES[key]
    meal = meal or T["meal"]
    cal = cal if cal is not None else T["cal"]
    protein = protein if protein is not None else T["pro"]

    maxv = max(T["dims"].values())
    dims_html = []
    for dim in DIM_ORDER:
        v = T["dims"][dim]
        pct = max(6, round(v / maxv * 100))
        h = 13 if v == maxv else 9
        dims_html.append(
            f'<div class="dim"><span class="l">{dim}</span>'
            f'<div class="t" style="height:{h}px"><i style="width:{pct}%;background:{T["color"]}"></i></div>'
            f'<span class="v">{pct}</span></div>'
        )
    rx_html = "".join(
        f'<div class="rx-row"><span>{html.escape(n)}</span><span class="dotline"></span>'
        f'<span class="qty">{html.escape(q)}</span></div>' for n, q in T["rx"]
    )
    code = "M" + datetime.now().strftime("%y%m%d%H%M")
    date_str = datetime.now().strftime("%Y.%m.%d")

    doc = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>麦太医 · 诊断证明书</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#F6F1E8;font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;
display:flex;justify-content:center;padding:22px 12px;color:#2B2118}}
.paper{{width:420px;max-width:100%;background:#FFFDF8;border:1px solid #E8DFD2;border-radius:14px;
overflow:hidden;box-shadow:0 14px 38px rgba(80,55,25,.13)}}
.head{{background:{T['color']};color:#fff;padding:15px 20px 13px;position:relative;overflow:hidden}}
.head::after{{content:"";position:absolute;right:-28px;top:-40px;width:120px;height:120px;
border-radius:50%;background:rgba(255,255,255,.12)}}
.clinic{{font-size:11px;letter-spacing:2.5px;opacity:.95}}
.title{{font-size:20px;font-weight:900;letter-spacing:5px;margin-top:5px}}
.meta{{display:flex;justify-content:space-between;padding:11px 20px;border-bottom:1px dashed #DCD0BE;
font-size:10.5px;color:#9A8A78;background:#FFF9EF}}
.meta b{{color:#5C4A38}}
.body{{padding:15px 20px 0}}
.sec{{font-size:11px;font-weight:800;letter-spacing:2px;color:{T['color']};margin:14px 0 7px}}
.sec:first-child{{margin-top:0}}
.chief{{font-size:13px;line-height:1.8;color:#5C5147}}
.name{{display:flex;align-items:center;gap:10px;margin-top:2px}}
.emoji{{font-size:32px}}
.tname{{font-size:22px;font-weight:900}}
.tag{{font-size:11.5px;color:#9A8A78;margin-top:2px}}
.dx{{margin-top:8px;display:inline-block;font-size:12px;font-weight:800;padding:5px 12px;
border-radius:20px;border:1px solid {T['color']};color:{T['color']}}}
.dim{{display:flex;align-items:center;gap:8px;font-size:11.5px;margin-bottom:7px}}
.dim .l{{width:30px;text-align:right;color:#8A7A68;flex-shrink:0}}
.dim .t{{flex:1;min-width:0;background:#F1E9DD;border-radius:5px;overflow:hidden}}
.dim .t i{{display:block;height:100%;border-radius:5px}}
.dim .v{{width:26px;color:#8A7A68;flex-shrink:0;font-size:10.5px}}
.rx{{background:#FFFDF3;border:1px solid #F0E4C8;border-radius:10px;padding:11px 13px}}
.rx-head{{font-size:15px;font-weight:900;font-style:italic;color:#8A5A1E;letter-spacing:1px}}
.rx-row{{display:flex;align-items:baseline;gap:6px;font-size:12.5px;margin-top:7px;color:#4A3B28}}
.rx-row .dotline{{flex:1;border-bottom:1px dotted #C9B896;transform:translateY(-3px)}}
.rx-row .qty{{font-weight:800;flex-shrink:0}}
.rx-usage{{margin-top:7px;font-size:10.5px;color:#A08A5E;line-height:1.65}}
.nut{{margin-top:9px;padding-top:8px;border-top:1px dashed #E3D5B4;font-size:11px;color:#8A5A1E;
display:flex;gap:12px}}
.advice{{font-size:12.5px;line-height:1.75;color:#3D5A4D;background:#EEF7F2;border-left:3px solid #2B8CC4;
border-radius:8px;padding:10px 12px}}
.sign{{display:flex;justify-content:space-between;align-items:flex-end;margin:16px 20px 0;
padding-top:11px;border-top:1px dashed #DCD0BE}}
.sign-l{{font-size:10.5px;color:#9A8A78;line-height:1.9}}
.sign-l b{{color:#3A2A1C;font-size:12px}}
.stamp{{width:56px;height:56px;border-radius:50%;border:2px solid {T['color']};color:{T['color']};
display:grid;place-items:center;font-size:8.5px;font-weight:800;transform:rotate(-12deg);
line-height:1.2;text-align:center;letter-spacing:.5px;opacity:.88}}
.foot{{padding:9px 20px 14px;font-size:9.5px;color:#B3A99E;line-height:1.7}}
</style></head><body>
<div class="paper">
  <div class="head">
    <div class="clinic">麦门综合门诊 · 营养科</div>
    <div class="title">诊断证明书</div>
  </div>
  <div class="meta">
    <span>患者：<b>麦门信徒</b></span><span>编号：<b>{code}</b></span><span>{date_str}</span>
  </div>
  <div class="body">
    <div class="sec">【主诉】</div>
    <p class="chief">{html.escape(T['chief'])}</p>
    <div class="sec">【诊断】</div>
    <div class="name"><span class="emoji">{T['emoji']}</span>
      <div><div class="tname">{html.escape(T['name'])}</div>
      <div class="tag">"{html.escape(T['tagline'])}"</div></div>
    </div>
    <div class="dx">{html.escape(T['dx'])}</div>
    <div class="sec">【口味基因检测】</div>
    {''.join(dims_html)}
    <div class="sec">【处方】</div>
    <div class="rx"><div class="rx-head">Rp.</div>{rx_html}
      <div class="nut"><span>约 <b>{cal}</b> kcal</span><span>蛋白质 <b>{protein}</b> g</span></div>
      <div class="rx-usage">用法用量：趁热服用，配冰可乐送服，每日不超过一次。</div>
    </div>
    <div class="sec">【医嘱】</div>
    <div class="advice">{html.escape(T['advice'])}</div>
  </div>
  <div class="sign">
    <div class="sign-l">主治医师：<b>麦太医</b><br>麦门综合门诊 · 营养科</div>
    <div class="stamp">麦门门诊<br>诊断专用章</div>
  </div>
  <div class="foot">本诊断仅供娱乐参考，不构成医疗、营养或其他专业建议。餐品与营养数据以麦当劳官方渠道实时结果为准。</div>
</div>
</body></html>"""

    out_dir = out_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"maitaiyi-dx-{key}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(doc)
    return out_path


def main():
    parser = argparse.ArgumentParser(description="麦太医 · 诊断证明书生成器")
    parser.add_argument("--type", required=True, choices=list(TYPES.keys()),
                        help="体质：spicy/bigmac/nuggets/cola/cone/fries")
    parser.add_argument("--meal", default=None)
    parser.add_argument("--cal", type=int, default=None)
    parser.add_argument("--protein", type=int, default=None)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    path = build_report_card(args.type, args.meal, args.cal, args.protein, args.out)
    print(json.dumps({"ok": True, "type": args.type, "name": TYPES[args.type]["name"],
                      "report": path}, ensure_ascii=False))
    print(f"诊断证明书已生成：{path}", file=sys.stderr)


if __name__ == "__main__":
    main()
