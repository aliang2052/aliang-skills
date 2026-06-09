# bailian-voice-clone · 百炼克隆音色语音合成

## 干什么

用你在百炼控制台**已创建的克隆音色**（CosyVoice v3.5-flash），通过 `bl speech synthesize` 合成语音。

这是一份"克隆音色合成说明书"：记录了正确的模型/参数组合，以及踩过的坑（比如克隆音色和系统音色是**不同模型**、不能混用）。

## 如何安装

需先安装百炼 CLI（见[仓库根 README](../../README.md#-前置依赖安装百炼-cli)），然后：

```bash
cp -R bailian-voice-clone ~/.claude/skills/
```

## ⚠️ 使用前：先创建你自己的克隆音色

- 声音克隆**必须在[百炼控制台](https://bailian.console.aliyun.com/)手动创建**（DashScope 的声音复刻 API 端点目前返回 404，无法用 CLI/SDK 直接创建）。
- 创建后拿到形如 `cosyvoice-v3.5-flash-xxxxx` 的完整 ID，替换 `SKILL.md` 里的 `YOUR_xxx_VOICE_ID` 占位符。
- 克隆音色绑定个人账号、无法共享。

## 如何使用

在 Claude Code 里说"用克隆音色合成……"，或直接用命令：

```bash
bl speech synthesize \
  --text "要合成的文本" \
  --model cosyvoice-v3.5-flash \
  --voice cosyvoice-v3.5-flash-你的音色ID \
  --out 输出.mp3 \
  --language zh
```

| 参数 | 说明 |
|------|------|
| `--model` | 克隆音色必须用 `cosyvoice-v3.5-flash` |
| `--voice` | 完整克隆音色 ID（含 `cosyvoice-v3.5-flash-` 前缀） |
| `--rate` | 语速 0.5–2.0（默认 1.0） |
| `--language` | `zh` / `en` |

> 系统音色（非克隆）请改用 `--model cosyvoice-v3-flash --voice longanyang` 这类。
