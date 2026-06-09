---
name: aliang-bailian-voice-clone
description: 使用百炼已创建的克隆音色（CosyVoice v3.5-flash）通过 bl speech synthesize 合成语音。
---

# 百炼克隆音色语音合成 Skill

## 触发词

当用户说"用阿亮的声音"、"克隆声音"、"声音合成"、"TTS"时使用。

## 重要发现

- **DashScope 声音复刻 API 端点**（`/compatible-mode/v1/audio/voices`）**返回 404**，无法通过 curl 或 SDK 直接创建克隆音色。
- 声音克隆必须在**百炼控制台**（console）中手动创建。
- 克隆音色创建后，可通过 `bl speech synthesize` 直接使用，传入完整的 voice ID 即可。

## 已有阿亮音色

| 场景 | 音色 ID |
|------|---------|
| 日常/温暖 | `cosyvoice-v3.5-flash-YOUR_WARM_VOICE_ID` |
| 科技风 | `cosyvoice-v3.5-flash-YOUR_TECH_VOICE_ID` |

## 使用方法

### 基本命令

```bash
bl speech synthesize \
  --text "{要合成的文本}" \
  --model cosyvoice-v3.5-flash \
  --voice {音色ID} \
  --out {输出路径.mp3} \
  --language zh
```

### 示例：用阿亮科技音色合成新闻

```bash
bl speech synthesize \
  --text "Anthropic 发布新一代旗舰模型 Claude Opus 4.8..." \
  --model cosyvoice-v3.5-flash \
  --voice cosyvoice-v3.5-flash-YOUR_TECH_VOICE_ID \
  --out 输出/阿亮科技新闻.mp3 \
  --language zh
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `--model` | 必须使用 `cosyvoice-v3.5-flash`（克隆音色专用模型） |
| `--voice` | 完整的克隆音色 ID（含前缀 `cosyvoice-v3.5-flash-`） |
| `--language` | `zh`（中文）或 `en`（英文） |
| `--rate` | 语速 0.5-2.0（默认 1.0） |
| `--pitch` | 音调 0.5-2.0（默认 1.0） |
| `--volume` | 音量 0-100（默认 50） |
| `--out` | 输出文件路径（mp3/wav/pcm/opus） |

## 注意事项

- `cosyvoice-v3-flash`（系统音色）和 `cosyvoice-v3.5-flash`（克隆音色）是**不同模型**，不能混用。
- 系统音色用 `--model cosyvoice-v3-flash --voice longanyang` 等。
- 克隆音色用 `--model cosyvoice-v3.5-flash --voice cosyvoice-v3.5-flash-xxx-xxx`。
- 如果用户需要新增克隆音色，需引导其前往百炼控制台操作，CLI 无法直接创建。
