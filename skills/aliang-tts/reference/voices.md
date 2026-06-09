# 阿亮音色信息

## 已创建的音色

| 名称 | Voice ID | 模型 | 风格描述 |
|------|----------|------|----------|
| 科技风 | `cosyvoice-v3.5-flash-YOUR_TECH_VOICE_ID` | cosyvoice-v3.5-flash | 科技播报，清晰有力 |
| 日常/温暖 | `cosyvoice-v3.5-flash-YOUR_WARM_VOICE_ID` | cosyvoice-v3.5-flash | 温暖自然，日常口播 |

## 合成参数

- 默认语速：`--rate 1.2`
- 默认语言：`--language zh`
- 默认输出目录：`输出/`

## 使用示例

```bash
# 科技风播报
bl speech synthesize \
  --text "播报内容" \
  --model cosyvoice-v3.5-flash \
  --voice cosyvoice-v3.5-flash-YOUR_TECH_VOICE_ID \
  --out 输出/xxx.mp3 \
  --language zh \
  --rate 1.2

# 日常风播报
bl speech synthesize \
  --text "播报内容" \
  --model cosyvoice-v3.5-flash \
  --voice cosyvoice-v3.5-flash-YOUR_WARM_VOICE_ID \
  --out 输出/xxx.mp3 \
  --language zh \
  --rate 1.2
```
