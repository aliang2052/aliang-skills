#!/usr/bin/env python3
"""Batch-generate short-drama key-frames from a storyboard.json using bl CLI.

Reads storyboard.json (see references/storyboard.md), and for each shot builds a
prompt = global style + per-shot character appearance + shot image_prompt, then
calls `bl image generate` (text-to-image) or `bl image edit` when a reference image
applies. Reference-image precedence per shot:
  character ref (locks a character's face/outfit) > global style_ref (locks the
  overall aesthetic from a poster/screenshot the user supplied) > none (text2img).
A default negative prompt is always applied. One PNG per shot.

The pipeline STOPS at images. Video is intentionally not generated here.

Usage:
  python3 gen_images.py --storyboard storyboard.json --outdir ./project
  python3 gen_images.py --storyboard storyboard.json --outdir ./project --only 1,2,5
  python3 gen_images.py --storyboard storyboard.json --outdir ./project --dry-run

Flags:
  --storyboard  Path to storyboard.json (required)
  --outdir      Output project dir; images go to <outdir>/images/ (required)
  --only        Comma-separated shot ids to (re)generate; default all
  --seed        Base seed for reproducibility (default 42); each character gets a stable offset
  --model       bl image model (default: qwen-image-2.0)
  --dry-run     Print the bl commands without running them
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

# 默认负向提示词：压制常见 AI 出图瑕疵
DEFAULT_NEGATIVE = "多余的手指，畸形的手，多余的肢体，错乱扭曲的文字，水印，签名，低清，模糊，jpeg噪点，比例失调"

# Aspect ratio -> Qwen-Image --size value
ASPECT_SIZE = {
    "9:16": "1080*1920",
    "16:9": "1920*1080",
    "1:1": "1024*1024",
    "3:4": "1080*1440",
    "4:3": "1440*1080",
}


def stable_offset(name: str) -> int:
    """Deterministic small offset per character name (no Math.random equivalent)."""
    return sum(ord(c) for c in name) % 1000


def build_prompt(shot: dict, style: str, char_map: dict) -> str:
    parts = []
    appearances = []
    for cname in shot.get("characters", []):
        c = char_map.get(cname)
        if c and c.get("desc"):
            appearances.append(f"{cname}（{c['desc']}）")
    if appearances:
        parts.append("人物：" + "；".join(appearances))
    parts.append("画面：" + shot["image_prompt"].strip())
    if style:
        parts.append("风格：" + style.strip())
    sz = shot.get("shot_size")
    if sz:
        parts.append(f"景别：{sz}")
    return "，".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--storyboard", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--only", default="")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--model", default="qwen-image-2.0")
    ap.add_argument("--negative", default=DEFAULT_NEGATIVE,
                    help="负向提示词；storyboard 里的 negative_prompt 优先")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    sb = json.loads(Path(args.storyboard).read_text(encoding="utf-8"))
    style = sb.get("style", "")
    aspect = sb.get("aspect", "9:16")
    size = ASPECT_SIZE.get(aspect, "1080*1920")
    char_map = {c["name"]: c for c in sb.get("characters", [])}
    # 全局风格参考图：用户甩的一张参考海报/截图，无角色 ref 的镜头用它当画风基准
    style_ref = sb.get("style_ref")
    negative = sb.get("negative_prompt") or args.negative

    only = set()
    if args.only.strip():
        only = {int(x) for x in args.only.split(",") if x.strip()}

    images_dir = Path(args.outdir) / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    shots = sb.get("shots", [])
    if not shots:
        print("storyboard 里没有 shots", file=sys.stderr)
        sys.exit(1)

    print(f"共 {len(shots)} 镜，画风：{style[:40]}...，比例 {aspect} ({size})")
    done = 0
    for shot in shots:
        sid = shot["id"]
        if only and sid not in only:
            continue
        prompt = build_prompt(shot, style, char_map)

        # Pick a stable seed: base + first character's offset (keeps a character's look steady)
        seed = args.seed
        chars = shot.get("characters", [])
        if chars:
            seed = args.seed + stable_offset(chars[0])

        prefix = f"shot_{sid:02d}"
        # 参考图优先级：角色基准图（锁脸）> 全局风格参考图（锁画风）> 无（纯文生图）
        char_ref = None
        if chars:
            c0 = char_map.get(chars[0]) or {}
            char_ref = c0.get("ref")
        ref_img = char_ref or style_ref
        ref_kind = "角色图" if char_ref else ("风格图" if style_ref else "无")

        if ref_img:
            # 带参考图：用 image edit 做风格/角色迁移；提示模型保留参考的画风或长相
            hint = "保持参考图中角色的长相与服装。" if char_ref else "保持参考图的整体画风、配色与质感。"
            cmd = [
                "bl", "image", "edit",
                "--image", ref_img,
                "--prompt", hint + prompt,
                "--size", size,
                "--seed", str(seed),
                "--negative-prompt", negative,
                "--out-dir", str(images_dir),
                "--out-prefix", prefix,
            ]
        else:
            cmd = [
                "bl", "image", "generate",
                "--prompt", prompt,
                "--model", args.model,
                "--size", size,
                "--seed", str(seed),
                "--negative-prompt", negative,
                "--out-dir", str(images_dir),
                "--out-prefix", prefix,
            ]

        print(f"\n[镜 {sid}] seed={seed} 参考={ref_kind}")
        print("  prompt:", prompt[:120] + ("..." if len(prompt) > 120 else ""))
        if args.dry_run:
            print("  CMD:", " ".join(f'"{x}"' if " " in x else x for x in cmd))
            continue
        # bl 出图偶发瞬时失败，自动重试最多 3 次
        ok = False
        for attempt in range(1, 4):
            try:
                subprocess.run(cmd, check=True)
                ok = True
                break
            except subprocess.CalledProcessError as e:
                print(f"  ⚠️ 镜 {sid} 第 {attempt}/3 次出图失败：{e}", file=sys.stderr)
        if ok:
            done += 1
        else:
            print(f"  ❌ 镜 {sid} 重试 3 次仍失败，跳过", file=sys.stderr)

    if not args.dry_run:
        print(f"\n✅ 完成 {done} 张，输出在 {images_dir}/")


if __name__ == "__main__":
    main()
