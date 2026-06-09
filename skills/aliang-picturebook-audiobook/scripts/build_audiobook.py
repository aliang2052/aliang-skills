#!/usr/bin/env python3
"""把一个 story.json 构建成有声绘本：逐段 TTS + 文生图，再合成网页版（+可选音频/视频）。

用法:
  build_audiobook.py --story story.json --outdir out [--style "..."] \
      [--web] [--merge-audio] [--video] [--all]

story.json 结构 (segments 数量任意)：
{
  "title": "书名",
  "characters": [{"name":"旁白","role":"narrator","trait":"温柔讲述者"}, ...],
  "segments": [
    {"id":1, "speaker":"旁白", "text":"要朗读的中文（对白用中文全角引号）",
     "emotion":"温柔讲述", "image_prompt":"该段画面描述",
     "voice":"<可选,覆盖默认音色>"}
  ]
}

依赖：bl (百炼 CLI) 必须可用；--video / --merge-audio 需要 ffmpeg。
"""
import argparse, json, subprocess, sys, shutil
from pathlib import Path

# 音色库（id, 性别 m/f/n, 标签）。选角导演从这里按角色性别/年龄/性格挑。
VOICE_CATALOG = [
    ("longniuniu_v3", "m", "阳光男童，活泼正气，适合男孩小英雄"),
    ("longjielidou_v3", "m", "顽皮男童，调皮机灵，适合捣蛋鬼/机智角色"),
    ("longze_v3", "m", "温暖元气男，少年感，适合温暖男角"),
    ("longcheng_v3", "m", "智慧青年男，沉稳，适合年长男角/王子"),
    ("longfei_v3", "m", "热血磁性男，豪迈，适合勇士/壮汉"),
    ("longtian_v3", "m", "磁性理智男，成熟低沉，适合爸爸/国王/旁白男声"),
    ("longhao_v3", "m", "多情忧郁男，柔和，适合温柔男角"),
    ("longlaotie_v3", "m", "东北直率男，憨厚搞笑，适合憨角/反派丑角"),
    ("longhuhu_v3", "f", "天真烂漫女童，软萌，适合小女孩/小动物"),
    ("longling_v3", "f", "稚气女童，奶声奶气，适合幼龄角色"),
    ("longxian_v3", "f", "豪放可爱女，活泼大方，适合假小子/活泼女孩"),
    ("longhua_v3", "f", "元气甜美女，明快，适合少女/小公主"),
    ("longanrou_v3", "f", "温柔娴静女，安静，适合温柔姐姐/妈妈"),
    ("longyan_v3", "f", "温暖春风女，亲切，适合妈妈讲故事/旁白"),
    ("longwan_v3", "f", "细腻柔声女，轻柔，适合温柔旁白/仙女"),
    ("longxiaoxia_v3", "f", "沉稳权威女，端庄，适合女王/奶奶/老师"),
    ("longshanshan_v3", "n", "戏剧化童声，夸张有趣，适合精灵/会说话的小物件"),
    ("longpaopao_v3", "n", "飞天泡泡音，奇幻空灵，适合精灵/魔法生物"),
]
DEFAULT_NARRATOR = "longyan_v3"   # 选角失败时旁白兜底
# 性别兜底池：按性别关键词命中后从对应池取，避免男角配女声这种错配
FALLBACK_M = ["longniuniu_v3", "longjielidou_v3", "longze_v3", "longfei_v3"]
FALLBACK_F = ["longhuhu_v3", "longhua_v3", "longxian_v3", "longanrou_v3"]
FALLBACK_N = ["longshanshan_v3", "longpaopao_v3", "longling_v3"]

# 情绪 -> (rate, pitch)。系统音色不支持 --instruction，只能用语速/音高表达情绪。
EMOTION_MAP = {
    "温柔讲述": (0.95, 1.00), "紧张转为安心": (0.97, 1.02), "害怕发抖": (0.92, 1.08),
    "坚定鼓励": (1.00, 0.95), "充满希望与力量": (1.00, 1.03), "欢快喜悦": (1.06, 1.06),
    "兴奋": (1.08, 1.05), "难过低落": (0.90, 0.96), "好奇": (1.02, 1.04),
}
DEFAULT_RP = (0.97, 1.00)

# 画风预设。--style 传预设名(key)则展开为下面的完整后缀；传其他文字则原样当作自定义画风。
STYLE_PRESETS = {
    "水彩绘本": "儿童绘本插画风格，柔和水彩，温暖治愈，圆润可爱的角色，明亮色调，统一画风，细腻光影",
    "国潮插画": "中国国潮插画风格，鲜艳撞色，描金线条，祥云纹样，传统神话元素现代化，活泼有张力，统一画风",
    "国风水墨": "中国风水墨工笔绘本，淡彩晕染，留白意境，毛笔线条，古典雅致，宣纸质感，统一画风",
    "剪纸民俗": "中国剪纸民俗风，红金配色，对称镂空纹样，喜庆年画感，平面装饰性强，统一画风",
    "皮克斯3D": "皮克斯3D卡通渲染，立体圆润，柔和光照，大眼可爱角色，电影质感，统一画风",
    "蜡笔手绘": "儿童蜡笔手绘风，稚拙笔触，温暖纸张质感，童真涂鸦感，柔和色块，统一画风",
    "扁平矢量": "扁平矢量插画，几何简洁，明快撞色，无渐变色块，现代绘本感，统一画风",
}
DEFAULT_STYLE = STYLE_PRESETS["水彩绘本"]


def resolve_style(s):
    """预设名→完整后缀；否则原样返回（自定义画风）。"""
    return STYLE_PRESETS.get(s, s)

TTS_MODEL = "cosyvoice-v3-flash"
IMG_MODEL = "qwen-image-2.0"
IMG_SIZE = "16:9"


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


GENDER_HINTS = {
    "m": ["男", "爸", "父", "爷", "哥", "弟", "叔", "伯", "王子", "国王", "公", "少年", "兄", "汉", "侠", "悟空", "哪吒", "猴"],
    "f": ["女", "妈", "母", "奶", "姐", "妹", "婶", "公主", "王后", "仙女", "姑娘", "少女", "婆", "娘"],
}


def _guess_gender(name, trait):
    s = name + (trait or "")
    fm = sum(s.count(k) for k in GENDER_HINTS["f"])
    mm = sum(s.count(k) for k in GENDER_HINTS["m"])
    return "f" if fm > mm else ("m" if mm > fm else "n")


def llm_cast(characters):
    """选角导演：让 bl 按性别/年龄/性格为每个角色挑最贴合的音色。返回 {name: voice_id}（已校验）。"""
    valid = {v[0] for v in VOICE_CATALOG}
    cat = "\n".join(f"{vid} | {'男' if g=='m' else '女' if g=='f' else '中性'} | {tag}" for vid, g, tag in VOICE_CATALOG)
    chars = "\n".join(f"- {c['name']}（{c.get('role','character')}）：{c.get('trait','')}" for c in characters)
    prompt = (f"你是有声书选角导演。可用音色库（id | 性别 | 气质）：\n{cat}\n\n"
              f"为这些角色各挑一个最贴合其性别、年龄、性格的音色：\n{chars}\n\n"
              "规则：男性角色只能用男声、女性角色只能用女声、性别不明的童话角色用中性童声；"
              "旁白用温暖适合讲故事的声音；不同角色尽量用不同音色。"
              "严格只输出 JSON：{\"角色名\":\"voice_id\"}，不要任何其它文字。")
    res = run(["bl", "text", "chat", "--message", prompt, "--output", "json"])
    try:
        content = json.loads(res.stdout)["choices"][0]["message"]["content"].strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1].rsplit("```", 1)[0]
        m = json.loads(content)
        return {k: v for k, v in m.items() if v in valid}
    except Exception:
        return {}


def assign_voices(segments, characters, auto_cast=True):
    """智能选角：优先 story 里显式 voice，其次 LLM 选角导演，再按性别启发式兜底。"""
    cmap = {c["name"]: c for c in characters}
    narrators = {c["name"] for c in characters if c.get("role") == "narrator"}
    narrators |= {"旁白", "narrator", "Narrator"}
    cast = llm_cast(characters) if auto_cast else {}
    used, fb_i = set(cast.values()), {"m": 0, "f": 0, "n": 0}

    def pick_fallback(name, trait, is_narrator):
        if is_narrator:
            return DEFAULT_NARRATOR
        g = _guess_gender(name, trait)
        pool = {"m": FALLBACK_M, "f": FALLBACK_F, "n": FALLBACK_N}[g]
        for _ in range(len(pool)):
            v = pool[fb_i[g] % len(pool)]; fb_i[g] += 1
            if v not in used:
                used.add(v); return v
        return pool[0]

    vmap = {}
    for s in segments:
        sp = s["speaker"]
        if sp in vmap:
            continue
        if s.get("voice"):
            vmap[sp] = s["voice"]
        elif sp in cast:
            vmap[sp] = cast[sp]
        else:
            trait = cmap.get(sp, {}).get("trait", "")
            vmap[sp] = pick_fallback(sp, trait, sp in narrators)
    return vmap


def synth(seg, voice, out):
    r, p = EMOTION_MAP.get(seg.get("emotion", ""), DEFAULT_RP)
    cmd = ["bl", "speech", "synthesize", "--text", seg["text"], "--voice", voice,
           "--model", TTS_MODEL, "--rate", str(r), "--pitch", str(p),
           "--format", "wav", "--out", str(out), "--quiet"]
    res = run(cmd)
    return res.returncode == 0 and out.exists(), (voice, r, p), res.stderr[-300:]


def gen_image(seg, style, outdir, prefix):
    prompt = f"{seg['image_prompt']}。{style}".replace('"', '')
    cmd = ["bl", "image", "generate", "--prompt", prompt, "--size", IMG_SIZE,
           "--model", IMG_MODEL, "--out-dir", str(outdir), "--out-prefix", prefix, "--quiet"]
    res = run(cmd)
    # bl 输出文件名通常是 <prefix>.png 或 <prefix>_0.png；统一规整成 <prefix>.png
    target = outdir / f"{prefix}.png"
    if not target.exists():
        cands = sorted(outdir.glob(f"{prefix}*.png"))
        if cands:
            cands[0].rename(target)
    return target.exists(), res.stderr[-300:]


def build_web(story, outdir, assets_dir):
    tpl = (assets_dir / "player_template.html").read_text()
    web = {"title": story["title"], "characters": story["characters"],
           "segments": [{"id": s["id"], "speaker": s["speaker"], "text": s["text"]}
                        for s in story["segments"]]}
    html = tpl.replace("/*__DATA__*/", json.dumps(web, ensure_ascii=False))
    html = html.replace("__TITLE__", story["title"])
    (outdir / "index.html").write_text(html)


def ffmpeg_ok():
    return shutil.which("ffmpeg") is not None


def merge_audio(story, outdir):
    seglist = outdir / "audio" / "_concat.txt"
    lines = [f"file 'seg_{s['id']:02d}.wav'" for s in story["segments"]]
    seglist.write_text("\n".join(lines))
    out = outdir / f"{story['title']}_audio.mp3"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(seglist),
         "-c:a", "libmp3lame", "-q:a", "2", str(out)])
    seglist.unlink(missing_ok=True)
    return out.exists()


def make_video(story, outdir):
    parts = []
    tmp = outdir / "_clips"; tmp.mkdir(exist_ok=True)
    for s in story["segments"]:
        n = f"{s['id']:02d}"
        img, aud = outdir/"images"/f"seg_{n}.png", outdir/"audio"/f"seg_{n}.wav"
        clip = tmp / f"clip_{n}.mp4"
        run(["ffmpeg", "-y", "-loop", "1", "-i", str(img), "-i", str(aud),
             "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
             "-pix_fmt", "yuv420p", "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2",
             "-shortest", str(clip)])
        if clip.exists(): parts.append(clip)
    lst = tmp / "list.txt"
    lst.write_text("\n".join(f"file '{c.name}'" for c in parts))
    out = outdir / f"{story['title']}.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c", "copy", str(out)])
    shutil.rmtree(tmp, ignore_errors=True)
    return out.exists()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--story", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--style", default=DEFAULT_STYLE)
    ap.add_argument("--web", action="store_true")
    ap.add_argument("--merge-audio", action="store_true")
    ap.add_argument("--video", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--skip-media", action="store_true", help="跳过 TTS/图片，仅重建网页")
    ap.add_argument("--no-auto-cast", action="store_true", help="关闭智能选角，用性别启发式兜底")
    a = ap.parse_args()
    if a.all: a.web = a.merge_audio = a.video = True
    if not (a.web or a.merge_audio or a.video): a.web = True  # 默认出网页
    a.style = resolve_style(a.style)
    print("🎨 画风:", a.style)

    assets_dir = Path(__file__).resolve().parent.parent / "assets"
    story = json.loads(Path(a.story).read_text())
    out = Path(a.outdir); (out/"audio").mkdir(parents=True, exist_ok=True); (out/"images").mkdir(exist_ok=True)

    vmap = assign_voices(story["segments"], story["characters"], auto_cast=not a.no_auto_cast)
    tagmap = {vid: tag for vid, g, tag in VOICE_CATALOG}
    print("🎙  智能选角:")
    for name, vid in vmap.items():
        print(f"    {name} → {vid}（{tagmap.get(vid, '—')}）")

    if not a.skip_media:
        for s in story["segments"]:
            n = f"{s['id']:02d}"; v = vmap[s["speaker"]]
            ok, info, err = synth(s, v, out/"audio"/f"seg_{n}.wav")
            print(f"  {'✅' if ok else '❌'} 配音 {n} {info}" + (f"  {err}" if not ok else ""))
            if not ok: sys.exit(f"TTS 失败于段 {n}")
            iok, ierr = gen_image(s, a.style, out/"images", f"seg_{n}")
            print(f"  {'✅' if iok else '❌'} 配图 {n}" + (f"  {ierr}" if not iok else ""))
            if not iok: sys.exit(f"图片失败于段 {n}")

    if a.web:
        build_web(story, out, assets_dir); print(f"🌐 网页版 -> {out/'index.html'}")
    if a.merge_audio or a.video:
        if not ffmpeg_ok(): sys.exit("需要 ffmpeg 才能导出音频/视频，请先安装 (brew install ffmpeg)")
    if a.merge_audio:
        print("🔊 音频合并:", "✅" if merge_audio(story, out) else "❌")
    if a.video:
        print("🎬 视频版:", "✅" if make_video(story, out) else "❌")
    print("🎉 完成 ->", out.resolve())


if __name__ == "__main__":
    main()
