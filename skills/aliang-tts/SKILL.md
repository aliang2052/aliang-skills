---
name: aliang-tts
description: 用阿亮的声音（科技风音色，1.2倍速）播报文字内容。支持纯文本、txt 文件、飞书文档链接。
type: skill
---

## 功能

用阿亮克隆音色将文本内容合成为语音文件，输出到 `输出/` 目录。

## 可用音色

> ⚠️ **音色 ID 需替换成你自己的**：克隆音色绑定个人百炼账号，无法共享。请先在
> [百炼控制台](https://bailian.console.aliyun.com/) 创建你的克隆音色（CosyVoice v3.5），
> 拿到形如 `cosyvoice-v3.5-flash-xxxxx` 的完整 ID，替换下表及 `scripts/tts.sh` 中的占位符。

| 音色 | Voice ID | 风格 |
|------|----------|------|
| 科技风 | `cosyvoice-v3.5-flash-YOUR_TECH_VOICE_ID` | 科技播报，清晰有力（默认） |
| 日常/温暖 | `cosyvoice-v3.5-flash-YOUR_WARM_VOICE_ID` | 温暖自然，日常口播 |

## 实现脚本

```bash
scripts/tts.sh "文本内容" [输出文件名.mp3] [voice_id]
```

## 输入支持

1. **纯文本**：直接传入要播报的文字
2. **txt 文件**：读取文件内容作为播报文本
3. **飞书文档链接**：用 `lark-doc` skill 读取文档内容，提取正文后播报

## 输出

- 文件路径：`声音/阿亮口播输出/`
- 格式：mp3
- 模型：`cosyvoice-v3.5-flash`
- 语速：1.2（默认）
- 文件名：`HHMMSS.mp3`（如 `101515.mp3`）

## 执行步骤

### 1. 判断输入类型

```python
if 输入包含 feishu.cn 或 lark 链接:
    → 用 lark-doc skill 读取文档内容，提取正文
elif 输入是 .txt 文件路径:
    → read_file 读取内容
else:
    → 直接使用输入文本
```

### 2. 生成文件名

```python
# 默认用当前时分秒
文件名 = HHMMSS + ".mp3"
# 如果指定了输出名，使用指定名
```

### 3. 调用合成脚本

```bash
bash scripts/tts.sh \
  "{处理后的文本}" \
  "{文件名}" \
  "{voice_id}"  # 可选，默认科技风
```

## 处理流程

```
输入类型判断
  ├── 纯文本 → 直接播报
  ├── .txt 文件 → read_file 读取内容 → 播报
  └── 飞书链接（feishu.cn/lark） → skill lark-doc 读取 → 提取正文 → 播报
```
