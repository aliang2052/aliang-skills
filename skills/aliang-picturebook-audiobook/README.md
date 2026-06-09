# aliang-picturebook-audiobook · 儿童有声绘本制作

<p align="center">
  <img src="../../assets/demo-picturebook.gif" width="440" alt="有声绘本动画 demo" />
</p>

## 干什么

给一个故事主题，做成一本**有声绘本**：

```
AI 写故事 → 分段 → 多音色配音(TTS) → 统一画风文生图 → 合成网页版翻页有声书
```

产物形态（可选）：

- **网页版**（默认）：单 HTML 翻页播放器，逐段大图 + 字幕 + 朗读，自动连播
- **mp4 视频版**：图片 + 音频合成视频，发抖音/视频号
- **纯音频 mp3**：各段合并，喜马拉雅/睡前播放

特点：旁白固定音色 + 角色轮流配音、7 种画风预设、用 emotion 控制语气。

## 如何安装

需先安装百炼 CLI（见[仓库根 README](../../README.md#-前置依赖安装百炼-cli)）。导出 mp4 / 合并音频还需 `ffmpeg`（仅要网页版则不需要）。然后：

```bash
cp -R aliang-picturebook-audiobook ~/.claude/skills/
```

## 如何使用

对你的 AI 助手说，例如：

```
把「小狐狸找月亮」做成有声绘本，6 段，水彩画风，再导出一个视频版
```

AI 会生成故事、让你选画风，然后自动逐段配音 + 配图并合成产物，最后 `open index.html` 预览。

## 目录结构

```
aliang-picturebook-audiobook/
├── SKILL.md
├── references/
│   ├── story_prompt.md       # 故事生成 prompt + 解析规则
│   ├── styles.md             # 7 种画风预设
│   └── voices.md             # 音色分配 / emotion 映射 / 避坑
├── scripts/
│   └── build_audiobook.py    # 配音+配图+组装一把梭
└── assets/
    └── player_template.html  # 网页翻页播放器模板
```
