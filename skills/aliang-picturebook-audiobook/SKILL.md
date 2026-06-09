---
name: aliang-picturebook-audiobook
description: 用阿里云百炼 bl CLI 把一个故事主题做成「儿童有声绘本」——AI 写故事→多音色配音(TTS)→统一画风文生图→合成网页版翻页有声书（可选导出 mp4 视频版、纯音频 mp3）。当用户想做有声书 / 有声绘本 / 儿童绘本 / 故事配音配图 / 睡前故事，或说"把故事做成有声书""做个绘本""故事变成声音再配图"时使用。
---

# 儿童有声绘本制作

把一个主题做成有声绘本：**AI 写故事 → 分段 → 多音色配音 → 统一画风配图 → 合成网页版（+可选视频/音频）**。全程用百炼 `bl` CLI，最后用本 skill 的脚本组装。

## 前置

- `bl` (百炼 CLI) 必须可用，已登录（`bl auth status` 可查）。
- 导出 mp4 / 合并音频需要 `ffmpeg`（网页版不需要）。

## 工作流（4 步）

开工前先和用户确认 2 件事（其余用默认）：**① 故事主题**（必问）；**② 要哪些产物**（网页版默认必出；是否再加 mp4 视频 / 纯音频 mp3）。段数默认 6、年龄默认 4-8 岁、画风默认水彩绘本，用户没特别要求就别追问。

### 1. 生成故事 → story.json

读 `references/story_prompt.md`，填好主题/段数，用 `bl text chat --message "<prompt>" --output json` 生成，按该文件的解析片段提取成 `story.json`。
- 若 `json.loads` 报错（多为对白用了英文引号），强调 prompt 第 7 条重新生成，**不要手工修补**。
- 生成后把 story.json 的角色/分段简要念给用户看一眼。

### 2. 选画风（按故事内容推荐，用户确认）

读 `references/styles.md`，按故事题材匹配出**推荐画风**，再用 AskUserQuestion 把 7 种预设给用户挑（推荐项放第一个标「(推荐)」）。例如中国神话题材推荐「国潮插画」。用户选定后作为下一步的 `--style` 值。

### 3. 配音 + 配图（脚本一把梭）

画风定了后，直接跑构建脚本，它会逐段 TTS + 文生图并组装产物：

```bash
python3 scripts/build_audiobook.py --story story.json --outdir <项目目录> --style <画风名> [--web] [--video] [--merge-audio] [--all]
```
- `--style` 传预设名（见 styles.md）即可；不传默认「水彩绘本」；也可传自定义画风描述文字。
- 不带产物标志默认只出网页版；`--all` = 网页+音频+视频。
- 音色自动分配（旁白固定 + 角色轮流），情绪用 rate/pitch 表达。**细节与坑见 `references/voices.md`，动手前务必读它**（最关键：系统音色加 `--instruction` 会报 428，所以禁止用 instruction）。多音色生效的前提是故事 segments 的 speaker 分给了不同角色（见 story_prompt.md 第 6 条）。
- 改了文字/换画风后只重跑：换 `--style` 重跑即可；只重建网页（不重出媒体）加 `--skip-media`。

### 4. 交付

产物在 `<项目目录>/`：`index.html`（网页版，双击或 `open` 即看）、`audio/seg_NN.wav`、`images/seg_NN.png`，以及可选 `<标题>.mp4`、`<标题>_audio.mp3`。最后用 `open index.html` 给用户预览。

## 产物形态

- **网页版**（默认）：单 HTML 翻页播放器，逐段大图+字幕+朗读，音频播完自动连播，支持上/下一段、进度条、圆点跳转、键盘 ←/→/空格。模板见 `assets/player_template.html`。
- **mp4 视频版**：图片+音频用 ffmpeg 合成 720p 视频，发抖音/视频号用。
- **纯音频 mp3**：各段合并成一个文件，喜马拉雅/睡前播放用。

## story.json 结构

```json
{
  "title": "书名",
  "characters": [{"name":"旁白","role":"narrator","trait":"温柔讲述者"}],
  "segments": [{"id":1,"speaker":"旁白","text":"朗读文字（对白用中文全角引号）",
    "emotion":"温柔讲述","image_prompt":"该段画面描述","voice":"<可选,覆盖音色>"}]
}
```
segments 数量任意；emotion 取值见 `references/voices.md` 的映射表。
