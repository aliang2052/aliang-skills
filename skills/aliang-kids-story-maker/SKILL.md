---
name: aliang-kids-story-maker
description: 儿童故事制作全流程：选择年龄→时长→播音风格→生成3个故事供选择→制作音频+插图→输出到指定目录。
---

# 儿童故事制作 Skill

## 触发词

当用户说"制作儿童故事"、"儿童故事"、"讲故事给孩子"、"睡前故事制作"时使用。

## 工作流

### 第一步：确认参数

向用户确认三个参数（如果用户未指定则使用默认值）：

**1. 孩子年龄**（3-12岁）

| 年龄段 | 内容特点 |
|--------|----------|
| 3-4岁 | 简单词汇，重复句式 |
| 5-6岁 | 稍有想象力，有情节 |
| 7-8岁 | 有冒险元素，稍复杂 |
| 9-10岁 | 有科普/成长主题 |
| 11-12岁 | 有深度，接近青少年 |

**2. 故事时长**

| 时长 | 字数 |
|------|------|
| 1分钟 | 约200-250字 |
| 2分钟 | 约400-500字 |
| 3分钟 | 约600-750字 |
| 5分钟 | 约1000-1200字 |

**3. 播音风格**（使用 cosyvoice-v3-flash 模型）

| 声音ID | 名称 | 风格 |
|--------|------|------|
| longanwen_v3 | 龙安温 | 温柔妈妈（默认） |
| longanyun_v3 | 龙安昀 | 知性女声 |
| longxiaochun_v3 | 龙小淳 | 可爱童声 |
| longhuhu_v3 | 龙呼呼 | 亲切叔叔 |
| longpaopao_v3 | 龙泡泡 | 活泼哥哥 |
| longfeifei_v3 | 龙菲菲 | 甜美姐姐 |

### 第二步：生成3个故事选项

使用 `bl text chat` 生成3个不同主题的故事标题+简介（每个50字左右），让用户选择。

Prompt 模板：

```
请为{age}岁的孩子生成3个不同的{duration}分钟睡前故事选项。
每个故事只需：标题（10字内）+ 一句话简介（30-50字）。
要求：
1. 3个故事主题完全不同
2. 适合{age}岁孩子的认知水平
3. 温暖、正面、有想象力
4. 格式：
【选项A】《标题》简介...
【选项B】《标题》简介...
【选项C】《标题》简介...
```

等待用户选择 A/B/C。

### 第三步：制作选定故事

根据用户选择，用 `bl text chat` 生成完整故事正文：

```
请为{age}岁的孩子写一个完整的{duration}分钟睡前故事，主题是"{selected_title}"。
要求：
1. 字数约{word_count}字
2. 语言口语化，适合电话/语音讲述
3. 温暖有趣，有想象力
4. 结尾有晚安/祝福
5. 只输出故事正文，不要其他说明
```

### 第四步：生成音频

```bash
bl speech synthesize --text "{story_text}" --model cosyvoice-v3-flash --voice {voice_id} --output /tmp/story_audio.mp3 --non-interactive
```

将输出文件复制到目标目录（CLI 默认输出到 `~/bailian-output/speech/`）。

### 第五步：生成插图

先用 `bl text chat` 从故事提取视觉描述：

```
请从以下故事中提取一段适合生成插图的英文描述（100词以内），适合{age}岁孩子：{story_text}
要求：描述画面主体人物、场景、氛围，适合水彩风格儿童绘本。不要包含文字说明。只输出英文描述。
```

然后生成图片：

```bash
bl image generate --prompt "A warm and dreamy children's book illustration for a {age}-year-old: {visual_desc}, soft watercolor style, warm golden and pastel color palette, magical bedtime atmosphere, no text" --out-dir /tmp/ --non-interactive
```

### 第六步：整理输出

1. 在 `声音/儿童故事/` 下新建文件夹，以故事标题命名（清理特殊字符）
2. 将以下文件放入：
   - `story.txt` — 故事文本
   - `audio.mp3` — 音频文件
   - `cover.png` — 插图
3. 向用户报告完成，列出文件路径

## 依赖

- Bailian CLI（bl 命令）
- cosyvoice-v3-flash（TTS）
- qwen-image-2.0（图片生成）
- 知识库凭证（如需要）：`~/.bailian-demo.env`
