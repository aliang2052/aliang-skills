# aliang-tts · 克隆音色文字播报

## 干什么

用你的**克隆音色**把文字内容合成为语音文件（mp3）。支持三种输入：

1. **纯文本** —— 直接传要播报的文字
2. **txt 文件** —— 读取文件内容播报
3. **飞书文档链接** —— 配合 `lark-doc` 技能读取正文后播报

默认科技风音色、1.2 倍速，可切日常/温暖音色。

## 如何安装

需先安装百炼 CLI（见[仓库根 README](../../README.md#-前置依赖安装百炼-cli)），然后：

```bash
cp -R aliang-tts ~/.claude/skills/
```

## ⚠️ 使用前：替换成你自己的音色 ID

克隆音色绑定个人百炼账号、**无法共享**，仓库内 ID 是占位符。请先：

1. 去[百炼控制台](https://bailian.console.aliyun.com/)创建你的克隆音色（CosyVoice v3.5），拿到形如 `cosyvoice-v3.5-flash-xxxxx` 的完整 ID
2. 把 `SKILL.md`、`reference/voices.md`、`scripts/tts.sh` 里的 `YOUR_TECH_VOICE_ID` / `YOUR_WARM_VOICE_ID` 占位符换成你的真实 ID

> 不想克隆？可直接改用系统音色（如 `longanwen_v3`），把 `--model` 换成 `cosyvoice-v3-flash`、`--voice` 填系统音色名即可。

## 如何使用

在 Claude Code 里说，例如：

```
用我的声音读一下这段：「大家好，今天聊聊 AI 的最新进展……」
```

或直接调脚本：

```bash
bash scripts/tts.sh "要播报的文本" [输出文件名.mp3] [voice_id]
```
